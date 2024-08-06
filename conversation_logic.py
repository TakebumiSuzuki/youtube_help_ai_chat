import constants as K
import os
import json
from dotenv import load_dotenv
from typing import List
import numpy as np
import time
import faiss
import google.generativeai as genai
from openai import OpenAI
import logging
import typing_extensions as typing


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

FAISS_PATH = K.FAISS_PATH
JSON_PATH = K.JSON_PATH

load_dotenv()
OPENAI_API_KEY = os.getenv(K.OPENAI_API_KEY)
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEYが.envファイル内に見つかりません")
    raise

GOOGLE_API_KEY = os.getenv(K.GOOGLE_API_KEY)
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEYが.envファイル内に見つかりません")
    raise

# FAISSインデックスの読み込み
try:
    index = faiss.read_index(FAISS_PATH)
    logger.info("FAISSインデックスの読み込みが正常に終了しました。")
except FileNotFoundError:
    logger.error(f"FAISSファイルが見つかりません: {FAISS_PATH}")
    raise
except Exception as e:
    logger.error(f"FAISSインデックスの読み込み中に不明のエラーが発生しました: {e}")
    raise


# JSONデータの読み込み
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    logger.info("JSONデータの読み込みが正常に終了しました。")
except FileNotFoundError:
    logger.error(f"JSONファイルが見つかりません: {JSON_PATH}")
    raise
except json.JSONDecodeError:
    logger.error(f"JSONファイルの解析に失敗しました: {JSON_PATH}")
    raise
except Exception as e:
    logger.error(f"JSONファイルの読み込み中に不明の問題が発生しました: {e}")
    raise


def get_hyde_query(orig_input: str) -> str:
    try:
        language = "English" if K.lang == "EN" else "Japanese"
        system_query = K.HYDE_PROMPT.format(language=language)

        start_time = time.time()

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model= K.OPENAI_HYDE_MODEL,
            messages=[
                {"role": "system", "content": system_query},
                {"role": "user", "content": orig_input},
                ]
        )
        hyde_query = response.choices[0].message.content

        end_time = time.time()  # 処理終了時刻を取得
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"処理時間: {elapsed_time:.3f}秒")  # 経過時間を表示

        # genai.configure(api_key=GOOGLE_API_KEY)
        # model = genai.GenerativeModel(K.GEMINI_HYDE_MODEL)
        # result = model.generate_content(system_query + orig_input)
        # hyde_query = result.text

        logger.info(f"HYDEクエリの作成が終了しました:")
        logger.info(f"{hyde_query}")

        return hyde_query

    except Exception as e:
        logger.error(f"HYDEクエリの生成中にエラーが発生しました: {e}")
        raise


def get_query_vector(hyde_query: str) -> np.ndarray:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            input=hyde_query,
            model=K.OPENAI_EMBEDDING_MODEL
        )
        query_vector = np.array([response.data[0].embedding]).astype('float32')

        # result = genai.embed_content(
        #     model=K.GEMINI_EMBEDDING_MODEL,
        #     content=hyde_query,
        #     task_type="retrieval_query",
        # )
        # query_vector = np.array([result['embedding']]).astype('float32')

        logger.info("クエリのembeddingベクトル生成が完了しました。")

        return query_vector

    except Exception as e:
        logger.error(f"クエリベクトルの生成中にエラーが発生しました: {e}")
        raise


def retrieve_docs(query_vector: np.ndarray) -> List[str]:
    try:
        distances, indices = index.search(query_vector, K.K)
        documents = []
        logger.info("ドキュメント(上位複数)の取得が完了しました。")

        for i in range(K.K):
            document = data[indices[0][i]]['content']
            documents.append(document)
            logger.info(f"類似度ランク {i+1}: 距離 {distances[0][i]}, インデックス {indices[0][i]}")

        return documents

    except Exception as e:
        logger.error(f"類似文書の検索中にエラーが発生しました: {e}")
        raise


def rerank_docs(orig_input, documents):
    text = ""
    for i, doc in enumerate(documents):
        text += f"index:{i} - {doc} \n"

    print('------------------')
    print(text)
    try:
        prompt = K.RERANK_PROMPT.format(orig_input=orig_input, text=text)

        start_time = time.time()
        class Indices(typing.TypedDict):
            top3_index: list[int]

        model = genai.GenerativeModel(
            K.GEMINI_RERANK_MODEL,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema" : Indices
        })

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.85,
                "top_k": 7,
                "max_output_tokens": 100,
            },
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"RERANK_処理時間: {elapsed_time:.3f}秒")

        print(response.text)
        response_obj = json.loads(response.text)
        return [documents[i] for i in response_obj['top3_index']]

    except Exception as e:
        logger.error(f"RERANKING中にエラーが発生しましたが、そのままQAに進みます: {e}")
        return documents[:4]


def retrieve_process(orig_input: str) -> str:
    try:
        hyde_query = get_hyde_query(orig_input)
        query_vector = get_query_vector(hyde_query)
        documents = retrieve_docs(query_vector)
        documents = rerank_docs(orig_input, documents)
        final_docs = "\n---\n".join(documents)
        return final_docs

    except Exception as e:
        logger.error(f"テキスト取得プロセス中にエラーが発生しました: {e}")
        raise




def get_stream(inputText: str, docs: str):
    try:
        language = "English" if K.lang == "EN" else "Japanese"

        qa_template = K.QA_PROMPT
        qa_base_prompt = qa_template.format(language=language, context=docs)
        system_prompt = f"{qa_base_prompt} + 'Here's the question: '"

        start_time = time.time()

        client = OpenAI(api_key=OPENAI_API_KEY)
        stream = client.chat.completions.create(
            model= K.OPENAI_QA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inputText},
            ],
            stream=True
        )

        # model = genai.GenerativeModel(K.GEMINI_QA_MODEL)
        # message = [{
        #     'role':'user',
        #     'parts': [prompt + inputText]
        # }]
        # stream = model.generate_content(message, stream=True)

        end_time = time.time()  # 処理終了時刻を取得
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"FINAL_QA_処理時間: {elapsed_time:.3f}秒")  # 経過時間を表示

        return stream

    except Exception as e:
        logger.error(f"ストリーム生成中にエラーが発生しました: {e}")
        raise






