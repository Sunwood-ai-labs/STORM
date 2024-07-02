import os
from dotenv import load_dotenv
from litellm import completion
from loguru import logger
from art import text2art

# .envファイルから環境変数を読み込む
load_dotenv()

class SlideConverter:
    def __init__(self, model="gemini/gemini-1.5-pro-latest"):
        self.model = model
        print(text2art("SlideConverter", font="slant"))
        logger.info(f"SlideConverterを初期化しました: モデル = {self.model}")

    def convert_to_slides(self, markdown_text):
        logger.info("スライド変換を開始します")
        
        try:
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "入力されたマークダウンテキストをReveal.js形式のスライドマークダウンに変換してください。各スライドは '---' で区切り、簡潔にまとめてください。"},
                    {"role": "user", "content": markdown_text}
                ]
            )
            
            slide_markdown = response['choices'][0]['message']['content']
            slide_markdown = slide_markdown.strip().lstrip('```markdown').rstrip('```').strip()
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
    import argparse
    
    parser = argparse.ArgumentParser(description="スライド変換ツール")
    parser.add_argument("-i", "--input", default="processed_text.md", help="入力マークダウンファイル名")
    parser.add_argument("-o", "--output", default="slides.md", help="出力スライドマークダウンファイル名")
    parser.add_argument("--model", default="gemini/gemini-1.5-pro-latest", help="使用するスライド変換モデル")
    
    args = parser.parse_args()
    
    logger.info("スライド変換モジュールを単独で実行します")
    
    markdown_text = read_markdown_file(args.input)
    
    if markdown_text:
        converter = SlideConverter(model=args.model)
        slide_markdown = converter.convert_to_slides(markdown_text)
        
        if slide_markdown:
            print(slide_markdown)
            converter.save_slides(slide_markdown, args.output)
    
    logger.info("スライド変換モジュールの実行を完了しました")