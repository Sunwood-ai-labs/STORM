import os
from dotenv import load_dotenv
from litellm import completion
from loguru import logger

# .envファイルから環境変数を読み込む
load_dotenv()

class SlideConverter:
    def __init__(self):
        self.model = "gemini/gemini-pro"

    def convert_to_slides(self, markdown_text):
        logger.info("スライド変換を開始します")
        
        try:
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "入力されたマークダウンテキストをスライド形式のマークダウンに変換してください。各スライドは '---' で区切り、内容を簡潔にまとめてください。"},
                    {"role": "user", "content": markdown_text}
                ]
            )
            
            slide_markdown = response['choices'][0]['message']['content']
            logger.success("スライド形式への変換が完了しました")
            return slide_markdown
        
        except Exception as e:
            logger.error(f"スライド変換中にエラーが発生しました: {str(e)}")
            return None

    def save_slides(self, slide_markdown, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(slide_markdown)
            logger.info(f"スライドマークダウンを {output_file} に保存しました")
        except Exception as e:
            logger.error(f"スライドマークダウンの保存中にエラーが発生しました: {str(e)}")

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"マークダウンファイルの読み込み中にエラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("スライド変換モジュールを単独で実行します")
    
    input_file = "processed_text.md"
    markdown_text = read_markdown_file(input_file)
    
    if markdown_text:
        converter = SlideConverter()
        slide_markdown = converter.convert_to_slides(markdown_text)
        
        if slide_markdown:
            print(slide_markdown)
            converter.save_slides(slide_markdown, "slides.md")
    
    logger.info("スライド変換モジュールの実行を完了しました")