# Python 3.11のベースイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_ENABLECORS true

# Streamlitのポートを公開
EXPOSE 8501



# Streamlitアプリケーションを実行
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]