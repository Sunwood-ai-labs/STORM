import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from pathlib import Path
from loguru import logger
from art import text2art

class WhisperSpeechRecognizer:
    def __init__(self):
        print(text2art("Whisper Speech Recognition", font="slant"))
        """Whisper音声認識モジュールの初期化"""
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        logger.info(f"デバイス: {self.device}, データ型: {self.torch_dtype}")
        
        model_id = "openai/whisper-large-v3"
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        
        self.processor = AutoProcessor.from_pretrained(model_id)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )
        
        logger.info("Whisper音声認識モジュールを初期化しました")

    def transcribe_audio(self, audio_file):
        """音声ファイルをテキストに変換"""
        logger.info(f"音声ファイル {audio_file} の認識を開始します")
        
        try:
            # datasetを使用せずに直接音声ファイルを読み込む
            result = self.pipe(audio_file)
            recognized_text = result["text"]
            logger.success("音声認識が完了しました")
            return recognized_text
        except Exception as e:
            logger.error(f"音声認識中にエラーが発生しました: {e}")
            return ""

def recognize_speech(audio_file):
    """音声ファイルを認識し、テキストを返す"""
    recognizer = WhisperSpeechRecognizer()
    return recognizer.transcribe_audio(audio_file)

def save_text_to_file(text, output_file):
    """テキストをファイルに保存"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.success(f"テキストを {output_file} に保存しました")
    except Exception as e:
        logger.error(f"テキストの保存中にエラーが発生しました: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Whisper音声認識ツール")
    parser.add_argument("-i", "--input", default="recorded_audio.wav", help="入力音声ファイル名")
    parser.add_argument("-o", "--output", default="recognized_text.txt", help="出力テキストファイル名")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        logger.error(f"指定された音声ファイル {input_path} が見つかりません")
    else:
        recognized_text = recognize_speech(str(input_path))
        if recognized_text:
            logger.info(f"認識されたテキスト: {recognized_text}")
            save_text_to_file(recognized_text, output_path)
        else:
            logger.warning("テキストを認識できませんでした")