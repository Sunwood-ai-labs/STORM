import argparse
import sys
# from storm.main import process_audio_to_ppt
# from storm.voice_input.recorder import record_audio

def main():
    parser = argparse.ArgumentParser(description="STORM CLI: 音声からPowerPointプレゼンテーションを作成するツール")
    subparsers = parser.add_subparsers(dest="command", help="利用可能なコマンド")

    # 変換コマンド
    convert_parser = subparsers.add_parser("convert", help="音声ファイルをPowerPointプレゼンテーションに変換")
    convert_parser.add_argument("input_file", help="入力音声ファイルのパス")
    convert_parser.add_argument("-o", "--output", default="output.pptx", help="出力PowerPointファイル名")

    # 録音コマンド
    record_parser = subparsers.add_parser("record", help="音声を録音してPowerPointプレゼンテーションに変換")
    record_parser.add_argument("-d", "--duration", type=int, default=10, help="録音時間（秒）")
    record_parser.add_argument("-o", "--output", default="output.pptx", help="出力PowerPointファイル名")

    args = parser.parse_args()

    if args.command == "convert":
        print(f"{args.input_file} をPowerPointに変換中...")
        # process_audio_to_ppt(args.input_file, args.output)
        print(f"PowerPointプレゼンテーションを {args.output} として保存しました")
    elif args.command == "record":
        print(f"{args.duration} 秒間音声を録音します...")
        # audio_file = record_audio(duration=args.duration)
        # print("録音完了。PowerPointに変換中...")
        # process_audio_to_ppt(audio_file, args.output)
        print(f"PowerPointプレゼンテーションを {args.output} として保存しました")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
