# Pythonベースイメージの指定
FROM python:3.11.7-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルのコピー
COPY requirements.txt .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . /app

# ポートの公開（Streamlitのデフォルトポート）
EXPOSE 8501

# アプリケーションの実行コマンド
CMD ["streamlit", "run", "app.py"]