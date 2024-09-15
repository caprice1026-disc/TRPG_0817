import os

# 基本設定
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///default.db')
#環境変数を一括で読み込むなどは後で考慮する
OPENAI_API_KEY = os.getenv(OPENAI_API_KEY)

# 機能フラグ(テンプレート 使用を考慮する)
FEATURE_X_ENABLED = True  # 機能Xを有効化
FEATURE_Y_ENABLED = False  # 機能Yを無効化

