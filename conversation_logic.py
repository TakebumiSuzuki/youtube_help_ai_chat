import constants as K
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import faiss
import numpy as np

# .env ファイルを読み込みPythonプロセス内のメモリに保存される。具体的には、os.environという辞書like オブジェクトに格納される。
# これらの変数はPythonプロセスの実行中のみ有効で、OSレベルの環境変数としては設定されない。つまり、他のプロセスやターミナルセッションからは見えない。
load_dotenv()
GOOGLE_API_KEY = os.getenv(K.GOOGLE_API_KEY)
FAISS_PATH = "./knowledge_data/JA_07_28_2024.faiss"
JSON_PATH = "./knowledge_data/JA_07_28_2024.json"

# FAISSインデックスの読み込み
index = faiss.read_index(FAISS_PATH)

try:
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
         data = json.load(file)
except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません。")
except json.JSONDecodeError:
    print(f"エラー: ファイルの解析に失敗しました。有効なJSONファイルであることを確認してください。")
except Exception as e:
    print(f"エラー: ファイルの読み込み中に不明の問題が発生しました: {e}")


def get_hyde_query(orig_input):

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')

    language = ("English" if K.lang == "EN" else "Japanese")
    query = K.HYDE_PROMPT.format(language=language) + orig_input

    result = model.generate_content(query)

    hyde_query = result.text
    print(hyde_query)
    return hyde_query


def get_query_vector(hyde_query):
    result = genai.embed_content(
            model="models/text-embedding-004",
            content=hyde_query,
            task_type="retrieval_query",
    )
    # result['embedding']は１次元配列なので[]でさらに括って２次元配列に
    query_vector = np.array([result['embedding']]).astype('float32')
    print('embedding 終わりました')
    return query_vector


def retrieve_docs(query_vector):
    distances, indices = index.search(query_vector, K.K)

    documents = []
    print("検索結果:")
    for i in range(K.K):
        print(f"類似度ランク {i+1}:")
        print(f"距離: {distances[0][i]}")
        print(f"インデックス: {indices[0][i]}")

        document = data[indices[0][i]]['content']
        print(f"ドキュメント: {document}")
        documents.append(document)

    return documents

def get_source_text(orig_input):
    hyde_query = get_hyde_query(orig_input)
    query_vector = get_query_vector(hyde_query)
    documents = retrieve_docs(query_vector)
    text = "\n---\n".join(documents)
    return text


def get_stream(inputText, docs):
    model = genai.GenerativeModel('gemini-1.5-flash')
    language = ("English" if K.lang == "EN" else "Japanese")

    qa_template = K.QA_PROMPT
    qa_base_prompt = qa_template.format(language=language, context=docs)
    prompt = f"{qa_base_prompt} + 'Here's the question: ' + {inputText}"

    message = [{
        'role':'user',
        'parts': [prompt]
        }]

    return model.generate_content(message, stream=True)


def error_handling(e):
    print(f"chunkのエラーです: {e}")










