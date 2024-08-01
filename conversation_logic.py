import constants as K
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import faiss
import numpy as np
import logging
from typing import List, Dict, Any

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# .env ファイルを読み込む
load_dotenv()
GOOGLE_API_KEY = os.getenv(K.GOOGLE_API_KEY)
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY が設定されていません。")
    raise EnvironmentError("GOOGLE_API_KEY が設定されていません。")

FAISS_PATH = "./knowledge_data/JA_07_28_2024.faiss"
JSON_PATH = "./knowledge_data/JA_07_28_2024.json"

# FAISSインデックスの読み込み
try:
    index = faiss.read_index(FAISS_PATH)
    logger.info("FAISSインデックスを正常に読み込みました。")
except FileNotFoundError:
    logger.error(f"FAISSファイルが見つかりません: {FAISS_PATH}")
    raise
except Exception as e:
    logger.error(f"FAISSインデックスの読み込み中にエラーが発生しました: {e}")
    raise

# JSONデータの読み込み
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
    logger.info("JSONデータを正常に読み込みました。")
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
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')

        language = "English" if K.lang == "EN" else "Japanese"
        query = K.HYDE_PROMPT.format(language=language) + orig_input

        result = model.generate_content(query)
        hyde_query = result.text
        logger.info("HYDEクエリを生成しました。")
        return hyde_query
    except Exception as e:
        logger.error(f"HYDEクエリの生成中にエラーが発生しました: {e}")
        raise

def get_query_vector(hyde_query: str) -> np.ndarray:
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=hyde_query,
            task_type="retrieval_query",
        )
        query_vector = np.array([result['embedding']]).astype('float32')
        logger.info("クエリベクトルを生成しました。")
        return query_vector
    except Exception as e:
        logger.error(f"クエリベクトルの生成中にエラーが発生しました: {e}")
        raise

def retrieve_docs(query_vector: np.ndarray) -> List[str]:
    try:
        distances, indices = index.search(query_vector, K.K)
        documents = []
        for i in range(K.K):
            document = data[indices[0][i]]['content']
            documents.append(document)
            logger.info(f"類似度ランク {i+1}: 距離 {distances[0][i]}, インデックス {indices[0][i]}")
        return documents
    except Exception as e:
        logger.error(f"類似文書の検索中にエラーが発生しました: {e}")
        raise

def retrieve_text(orig_input: str) -> str:
    try:
        hyde_query = get_hyde_query(orig_input)
        query_vector = get_query_vector(hyde_query)
        documents = retrieve_docs(query_vector)
        text = "\n---\n".join(documents)
        logger.info("テキストの取得が完了しました。")
        return text
    except Exception as e:
        logger.error(f"テキスト取得プロセス中にエラーが発生しました: {e}")
        raise

def get_stream(inputText: str, docs: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        language = "English" if K.lang == "EN" else "Japanese"

        qa_template = K.QA_PROMPT
        qa_base_prompt = qa_template.format(language=language, context=docs)
        prompt = f"{qa_base_prompt} + 'Here's the question: ' + {inputText}"

        message = [{
            'role':'user',
            'parts': [prompt]
        }]

        stream = model.generate_content(message, stream=True)
        logger.info("ストリーム生成を開始しました。")
        return stream
    except Exception as e:
        logger.error(f"ストリーム生成中にエラーが発生しました: {e}")
        raise

def error_handling(e: Exception):
    logger.error(f"エラーが発生しました: {e}")
    # ここでエラーに応じた適切な処理を行う
    # 例: ユーザーへの通知、再試行ロジック、エラーレポートの送信など