import prompt_constants as PC
import config_constants as CC
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

load_dotenv()
OPENAI_API_KEY = os.getenv(CC.OPENAI_API_KEY)
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEYが.envファイル内に見つかりません")
    raise

# GEMINI_API_KEY = os.getenv(CC.GEMINI_API_KEY)
# if not GEMINI_API_KEY:
#     logger.error("GEMINI_API_KEYが.envファイル内に見つかりません")
#     raise

# FAISSインデックスの読み込み
loaded_faiss = {}
for lang, file_path in CC.FAISS_FILES.items():
    try:
        loaded_faiss[lang] = faiss.read_index(file_path)
    except FileNotFoundError:
        logger.error(f"FAISSファイルが見つかりません: {file_path}")
        raise
    except Exception as e:
        logger.error(f"FAISSインデックス {file_path} の読み込み中に不明のエラーが発生しました: {e}")
        raise

logger.info("すべてのFAISSインデックスの読み込みが正常に終了しました。")


# JSONデータの読み込み
loaded_json = {}
for lang, file_path in CC.JSON_FILES.items():
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_json[lang] = json.load(file)
    except FileNotFoundError:
        logger.error(f"JSONファイルが見つかりません: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"JSONファイルの解析に失敗しました: {file_path}")
        raise
    except Exception as e:
        logger.error(f"JSONファイル {file_path} の読み込み中に不明の問題が発生しました: {e}")
        raise

logger.info("すべてのJSONデータの読み込みが正常に終了しました。")


def get_databases(language):
    if language == 'Japanese':
        return loaded_faiss['ja'], loaded_json['ja']
    elif language == 'Spanish':
        return loaded_faiss['es'], loaded_json['es']
    elif language == 'Indonesian':
        return loaded_faiss['id'], loaded_json['id']
    else:
        return loaded_faiss['en'], loaded_json['en']




def get_hyde_query(orig_input: str) -> str:
    try:
        system_query = PC.HYDE_PROMPT

        start_time = time.time()

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model= CC.OPENAI_HYDE_MODEL,
            messages=[
                {"role": "system", "content": system_query},
                {"role": "user", "content": orig_input},
                ]
        )
        hyde_query = response.choices[0].message.content


        # genai.configure(api_key=GEMINI_API_KEY)
        # model = genai.GenerativeModel(CC.GEMINI_HYDE_MODEL)
        # result = model.generate_content(system_query + orig_input)
        # hyde_query = result.text

        logger.info(f"HYDEクエリの作成が終了しました:")
        logger.info(CC.OPENAI_HYDE_MODEL)
        logger.info(f"{hyde_query}")
        end_time = time.time()  # 処理終了時刻を取得
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"GET_HYDE_QUERY_処理時間: {elapsed_time:.3f}秒")  # 経過時間を表示

        return hyde_query

    except Exception as e:
        logger.error(f"HYDEクエリの生成中にエラーが発生しました: {e}")
        raise


def split_last_brackets(input_string):
    # 文字列を逆順に並べ替える
    reversed_string = input_string[::-1]
    # 最初の開き中括弧を見つける
    start_index = reversed_string.find('[')
    # 見つかった開き中括弧の位置をもとの文字列の位置に戻す
    end_index = len(input_string) - start_index
    # 最後の中括弧の部分を抽出
    prompt_part = input_string[:end_index]
    bracket_part = input_string[end_index:]

    return prompt_part, bracket_part


def extract_language(text: str) -> str:
    if 'japanese' in text.lower():
        return 'Japanese'
    elif 'spanish' in text.lower():
        return 'Spanish'
    elif 'indonesian' in text.lower():
        return 'Indonesian'
    else:
        return 'English'



def get_query_vector(hyde_query: str) -> np.ndarray:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            input=hyde_query,
            model=CC.OPENAI_EMBEDDING_MODEL
        )
        query_vector = np.array([response.data[0].embedding]).astype('float32')

        # result = genai.embed_content(
        #     model=CC.GEMINI_EMBEDDING_MODEL,
        #     content=hyde_query,
        #     task_type="retrieval_query",
        # )
        # query_vector = np.array([result['embedding']]).astype('float32')

        logger.info("クエリのembeddingベクトル生成が完了しました。")

        return query_vector

    except Exception as e:
        logger.error(f"クエリベクトルの生成中にエラーが発生しました: {e}")
        raise


def retrieve_docs(query_vector: np.ndarray, language: str) -> List[str]:
    try:
        faiss, json = get_databases(language)
        distances, indices = faiss.search(query_vector, CC.K)
        documents = []
        logger.info("ドキュメント(上位複数)の取得が完了しました。")

        for i in range(CC.K):
            document = json[indices[0][i]]['content']
            documents.append(document)
            logger.info(f"類似度ランク {i+1}: 距離 {distances[0][i]}, インデックス {indices[0][i]}")

        return documents

    except Exception as e:
        logger.error(f"類似文書の検索中にエラーが発生しました: {e}")
        raise





def handle_retrieval(orig_input: str) -> str:
    try:
        hyde_query = get_hyde_query(orig_input)
        hyde_query, bracket_part = split_last_brackets(hyde_query)
        language = extract_language(bracket_part)
        query_vector = get_query_vector(hyde_query)
        documents = retrieve_docs(query_vector, language)
        # documents = rerank_docs(orig_input, documents)
        final_docs = "\n---\n".join(documents)
        return final_docs, language

    except Exception as e:
        logger.error(f"テキスト取得プロセス中にエラーが発生しました: {e}")
        raise




def get_stream(inputText: str, docs: str, language: str):
    try:
        qa_template = PC.QA_PROMPT
        qa_base_prompt = qa_template.format(language=language, context=docs)
        system_prompt = f"{qa_base_prompt} + 'Here's the question: '"
        print(qa_base_prompt)
        start_time = time.time()

        client = OpenAI(api_key=OPENAI_API_KEY)
        stream = client.chat.completions.create(
            model= CC.OPENAI_QA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inputText},
            ],
            stream=True
        )

        # model = genai.GenerativeModel(CC.GEMINI_QA_MODEL)
        # message = [{
        #     'role':'user',
        #     'parts': [prompt + inputText]
        # }]
        # stream = model.generate_content(message, stream=True)
        logger.info(CC.OPENAI_QA_MODEL)
        end_time = time.time()  # 処理終了時刻を取得
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"FINAL_QA_処理時間: {elapsed_time:.3f}秒")  # 経過時間を表示

        return stream

    except Exception as e:
        logger.error(f"ストリーム生成中にエラーが発生しました: {e}")
        raise





# def rerank_docs(orig_input, documents):
#     text = ""
#     for i, doc in enumerate(documents):
#         text += f"index:{i} - {doc} \n"

#     print('------------------')
#     print(text)
#     try:
#         prompt = CC.RERANK_PROMPT.format(orig_input=orig_input, text=text)

#         start_time = time.time()
#         class Indices(typing.TypedDict):
#             top3_index: list[int]

#         model = genai.GenerativeModel(
#             CC.GEMINI_RERANK_MODEL,
#             generation_config={
#                 "response_mime_type": "application/json",
#                 "response_schema" : Indices
#         })

#         response = model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0.2,
#                 "top_p": 0.85,
#                 "top_k": 7,
#                 "max_output_tokens": 100,
#             },
#         )
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         print(f"RERANK_処理時間: {elapsed_time:.3f}秒")

#         print(response.text)
#         response_obj = json.loads(response.text)
#         return [documents[i] for i in response_obj['top3_index']]

#     except Exception as e:
#         logger.error(f"RERANKING中にエラーが発生しましたが、そのままQAに進みます: {e}")
#         return documents[:4]






