import os
from dotenv import load_dotenv
from interpreter import interpreter

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key is None:
    raise ValueError("ANTHROPIC_API_KEY is not set in the .env file")

os.environ["ANTHROPIC_API_KEY"] = api_key
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")


# 生成したコードを自動的に実行するように設定。実行すべきではないコードが生成される可能性もあるため注意して利用すること
interpreter.auto_run = True

# 利用するモデルを設定
# interpreter.llm.model = "anthropic/claude-3-5-sonnet-20240620"
interpreter.llm.model = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"

# モデルのコンテキストウィンドウサイズを設定
interpreter.llm.context_window = 8000  # type: ignore

message = """

Gitを使用して今のリポジトリで変更があったファイルごとにコミットメッセージを作成してコミットしてください
- コミットメッセージは下記のフォーマットと種類に従って作成してください
- 日本語で対応してください
- OSはWindowsです

## コミットメッセージの種類
コミットメッセージの種類は下記を参考にして

例：
  - feat: 新機能
  - fix: バグ修正
  - docs: ドキュメントのみの変更
  - style: コードの動作に影響しない変更（空白、フォーマット、セミコロンの欠落など） 
  - refactor: バグの修正も機能の追加も行わないコードの変更
  - perf: パフォーマンスを向上させるコードの変更
  - test: 欠けているテストの追加や既存のテストの修正
  - chore: ビルドプロセスやドキュメント生成などの補助ツールやライブラリの変更


## コミットメッセージのフォーマット

(コミットメッセージに最適な絵文字) [種類] 概要


"""
interpreter.chat(message, display=True, stream=False)

# 途中でユーザーからの入力待ちになるので、処理を続行するよう指示
interpreter.chat("続けてください。", display=True, stream=False)