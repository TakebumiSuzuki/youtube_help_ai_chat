import ui_constants as UC

# OpenAIを使用した場合の設定項目
OPENAI_API_KEY = 'OPENAI_API_KEY'
OPENAI_HYDE_MODEL = 'gpt-4o-2024-08-06'
OPENAI_EMBEDDING_MODEL = 'text-embedding-3-large'
OPENAI_QA_MODEL = 'gpt-4o-2024-08-06'

# Geminiを使用した場合の設定項目
# GEMINI_API_KEY = 'GEMINI_API_KEY'
# GEMINI_HYDE_MODEL = 'gemini-1.5-flash-latest'
# GEMINI_EMBEDDING_MODEL = 'models/text-embedding-004' # 英語のみの対応
# GEMINI_QA_MODEL = 'models/gemini-1.5-pro-latest'
# GEMINI_RERANK_MODEL = 'gemini-1.5-pro-exp-0801'


K = 4

# データファイルのパス設定
FAISS_FILES = {
    UC.JAPANESE: "./knowledge_data/JA_08_02_2024_V3.faiss",
    UC.SPANISH: "./knowledge_data/ES_08_07_2024.faiss",
    UC.INDONESIAN: "./knowledge_data/ID_08_12_2024.faiss",
    UC.KOREAN: "./knowledge_data/KO_08_12_2024.faiss",
    UC.VIETNAMESE: "./knowledge_data/VI_08_14_2024.faiss",
    UC.THAI: "./knowledge_data/TH_08_19_2024.faiss",
    UC.ENGLISH: "./knowledge_data/EN_08_07_2024.faiss"
}

JSON_FILES = {
    UC.JAPANESE: "./knowledge_data/JA_08_02_2024_V3.json",
    UC.SPANISH: "./knowledge_data/ES_08_07_2024.json",
    UC.INDONESIAN: "./knowledge_data/ID_08_12_2024.json",
    UC.KOREAN: "./knowledge_data/KO_08_12_2024.json",
    UC.VIETNAMESE: "./knowledge_data/VI_08_14_2024.json",
    UC.THAI: "./knowledge_data/TH_08_19_2024.json",
    UC.ENGLISH: "./knowledge_data/EN_08_07_2024.json"
}

# GEMINIのセーフティセッティングで使う
# safety_settings = [
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_NONE",
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_NONE",
#     },
# ]

