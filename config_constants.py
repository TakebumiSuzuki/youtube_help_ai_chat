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

# データファイルのパス設定
FAISS_FILES = {
    'ja': "./knowledge_data/JA_08_02_2024_V3.faiss",
    'es': "./knowledge_data/JA_08_02_2024_V3.faiss",
    'ko': "./knowledge_data/JA_08_02_2024_V3.faiss",
    'en': "./knowledge_data/EN_08_07_2024.faiss"
}

JSON_FILES = {
    'ja': "./knowledge_data/JA_08_02_2024_V3.json",
    'es': "./knowledge_data/JA_08_02_2024_V3.json",
    'ko': "./knowledge_data/JA_08_02_2024_V3.json",
    'en': "./knowledge_data/EN_08_07_2024.json"
}

K = 4