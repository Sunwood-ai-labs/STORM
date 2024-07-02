import argparse
import sys
from storm.voice_input.recorder import record_audio
from storm.speech_recognition.whisper_speech_recognition import recognize_speech
from storm.text_processing.text_processor import TextProcessor
from storm.slide_conversion.slide_converter import SlideConverter
from storm.ppt_conversion.ppt_converter import PowerPointConverter

def main():
    from art import text2art
    print(text2art(" Welcome to STORM !!", font="slant"))

    parser = argparse.ArgumentParser(description="STORM CLI: 音声からPowerPointプレゼンテーションを作成するツール")
    parser.add_argument("--mode", nargs="+", choices=["all", "record", "recognize", "process", "slides", "ppt"], 
                        default=["all"], help="実行するモードを指定（複数選択可）")
    
    # 各モジュールの入出力ファイルを指定するオプションを追加
    parser.add_argument("--record-output", default="recorded_audio.wav", help="録音の出力ファイル")
    parser.add_argument("--recognize-input", default="recorded_audio.wav", help="音声認識の入力ファイル")
    parser.add_argument("--recognize-output", default="recognized_text.txt", help="音声認識の出力ファイル")
    parser.add_argument("--process-input", default="recognized_text.txt", help="テキスト処理の入力ファイル")
    parser.add_argument("--process-output", default="processed_text.md", help="テキスト処理の出力ファイル")
    parser.add_argument("--slides-input", help="スライド変換の入力ファイル")
    parser.add_argument("--slides-output", default="slides.md", help="スライド変換の出力ファイル")
    parser.add_argument("--ppt-input", help="PowerPoint変換の入力ファイル")
    parser.add_argument("--ppt-output", default="output.pptx", help="PowerPoint変換の出力ファイル")
    
    parser.add_argument("-d", "--duration", type=int, default=10, help="録音時間（秒）")
    parser.add_argument("-t", "--template", default="template.pptx", help="PowerPointテンプレートファイル")
    
    # 新しい引数を追加
    parser.add_argument("--asr-model", default="openai/whisper-large-v3", help="音声認識モデル")
    parser.add_argument("--text-model", default="claude-3-haiku-20240307", help="テキスト処理モデル")
    parser.add_argument("--slide-model", default="claude-3-haiku-20240307", help="スライド変換モデル")
    parser.add_argument("--sample-rate", type=int, default=44100, help="録音のサンプルレート")
    parser.add_argument("--channels", type=int, default=1, help="録音のチャンネル数")

    args = parser.parse_args()

    # 'all' モードが選択されている場合、全てのモードを実行
    if "all" in args.mode:
        modes = ["record", "recognize", "process", "slides", "ppt"]
    else:
        modes = args.mode

    if "record" in modes:
        output_file = args.record_output
        input_file = record_audio(duration=args.duration, output_file=output_file, 
                                  rate=args.sample_rate, channels=args.channels)
        print(f"音声を録音し、{output_file}として保存しました")

    if "recognize" in modes:
        input_file = args.recognize_input or input_file
        if not input_file:
            print("音声ファイルを指定してください")
            sys.exit(1)
        output_file = args.recognize_output
        recognized_text = recognize_speech(input_file, model_id=args.asr_model)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(recognized_text)
        print(f"音声をテキストに変換し、{output_file}として保存しました")

    if "process" in modes:
        input_file = args.process_input or input_file
        if not input_file:
            print("テキストファイルを指定してください")
            sys.exit(1)
        output_file = args.process_output
        processor = TextProcessor(model=args.text_model)
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        processed_markdown = processor.process_text(input_text)
        processor.save_markdown(processed_markdown, output_file)
        print(f"テキストを処理し、{output_file}として保存しました")

    if "slides" in modes:
        input_file = args.slides_input or input_file
        if not input_file:
            print("マークダウンファイルを指定してください")
            sys.exit(1)
        output_file = args.slides_output
        converter = SlideConverter(model=args.slide_model)
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        slide_markdown = converter.convert_to_slides(markdown_text)
        converter.save_slides(slide_markdown, output_file)
        print(f"スライドを作成し、{output_file}として保存しました")

    if "ppt" in modes:
        input_file = args.ppt_input or input_file
        if not input_file:
            print("スライドマークダウンファイルを指定してください")
            sys.exit(1)
        output_file = args.ppt_output
        converter = PowerPointConverter(template_path=args.template)
        converter.convert(input_file, output_file)
        print(f"PowerPointプレゼンテーションを{output_file}として保存しました")

    print("処理が完了しました")

if __name__ == "__main__":
    main()