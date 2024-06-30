import os
from dotenv import load_dotenv
from litellm import completion
from loguru import logger
from art import text2art

# .envファイルから環境変数を読み込む
load_dotenv()

class TextProcessor:
    def __init__(self):
        # ASCIIアートでクラス名を表示
        print(text2art("TextProcessor", font="slant"))
        self.model = "gemini/gemini-pro"

    def process_text(self, input_text):
        logger.info("テキスト処理を開始します")
        
        try:
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "入力されたテキストを解析し、基本的なマークダウン形式で構造化してください。見出し、リスト、強調などのマークダウン要素を適切に使用してください。"},
                    {"role": "user", "content": input_text}
                ]
            )
            
            markdown_text = response['choices'][0]['message']['content']
            logger.success("テキストの構造化が完了しました")
            return markdown_text
        
        except Exception as e:
            logger.error(f"テキスト処理中にエラーが発生しました: {str(e)}")
            return None

    def save_markdown(self, markdown_text, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            logger.info(f"マークダウンを {output_file} に保存しました")
        except Exception as e:
            logger.error(f"マークダウンの保存中にエラーが発生しました: {str(e)}")

def read_input_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"入力ファイルの読み込み中にエラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("テキスト処理モジュールを単独で実行します")
    
    input_file = "input_text.txt"
    input_text = read_input_file(input_file)
    
    if input_text:
        processor = TextProcessor()
        processed_markdown = processor.process_text(input_text)
        
        if processed_markdown:
            print(processed_markdown)
            processor.save_markdown(processed_markdown, "processed_text.md")
    
    logger.info("テキスト処理モジュールの実行を完了しました")