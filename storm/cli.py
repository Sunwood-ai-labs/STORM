import argparse
import sys
from storm.voice_input.recorder import record_audio
from storm.speech_recognition.whisper_speech_recognition import recognize_speech
from storm.text_processing.text_processor import TextProcessor
from storm.slide_conversion.slide_converter import SlideConverter
from storm.ppt_conversion.ppt_converter import PowerPointConverter

def main():
    parser = argparse.ArgumentParser(description="STORM CLI: 音声からPowerPointプレゼンテーションを作成するツール")
    parser.add_argument("--mode", nargs="+", choices=["record", "recognize", "process", "slides", "ppt"], 
                        help="実行するモードを指定（複数選択可）")
    parser.add_argument("-i", "--input", help="入力ファイル")
    parser.add_argument("-o", "--output", help="出力ファイル")
    parser.add_argument("-d", "--duration", type=int, default=10, help="録音時間（秒）")
    parser.add_argument("-t", "--template", default="template.pptx", help="PowerPointテンプレートファイル")

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    input_file = args.input
    output_file = args.output

    if "record" in args.mode:
        output_file = output_file or "recorded_audio.wav"
        input_file = record_audio(duration=args.duration, output_file=output_file)
        print(f"音声を録音し、{output_file}として保存しました")

    if "recognize" in args.mode:
        if not input_file:
            print("音声ファイルを指定してください")
            sys.exit(1)
        output_file = output_file or "recognized_text.txt"
        recognized_text = recognize_speech(input_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(recognized_text)
        print(f"音声をテキストに変換し、{output_file}として保存しました")
        input_file = output_file

    if "process" in args.mode:
        if not input_file:
            print("テキストファイルを指定してください")
            sys.exit(1)
        output_file = output_file or "processed_text.md"
        processor = TextProcessor()
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        processed_markdown = processor.process_text(input_text)
        processor.save_markdown(processed_markdown, output_file)
        print(f"テキストを処理し、{output_file}として保存しました")
        input_file = output_file

    if "slides" in args.mode:
        if not input_file:
            print("マークダウンファイルを指定してください")
            sys.exit(1)
        output_file = output_file or "slides.md"
        converter = SlideConverter()
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        slide_markdown = converter.convert_to_slides(markdown_text)
        converter.save_slides(slide_markdown, output_file)
        print(f"スライドを作成し、{output_file}として保存しました")
        input_file = output_file

    if "ppt" in args.mode:
        if not input_file:
            print("スライドマークダウンファイルを指定してください")
            sys.exit(1)
        output_file = output_file or "output.pptx"
        converter = PowerPointConverter(template_path=args.template)
        converter.convert(input_file, output_file)
        print(f"PowerPointプレゼンテーションを{output_file}として保存しました")

    print("処理が完了しました")

if __name__ == "__main__":
    main()