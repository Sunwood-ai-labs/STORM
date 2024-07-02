import pyaudio
import wave
import numpy as np
from pathlib import Path
from loguru import logger
from art import text2art

class AudioRecorder:
    def __init__(self, rate=44100, channels=1, chunk=1024):
        """オーディオレコーダーの初期化"""
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        self.frames = []
        print(text2art("AudioRecorder", font="slant"))
        logger.info(f"オーディオレコーダーを初期化しました: サンプルレート={rate}, チャンネル数={channels}")


    def start_recording(self, duration):
        """指定された時間だけ録音を開始"""
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.chunk)

        logger.info("録音を開始しました")
        total_chunks = int(self.rate / self.chunk * duration)
        for i in range(total_chunks):
            data = stream.read(self.chunk)
            self.frames.append(data)
            if i % 10 == 0:  # 10チャンクごとに進捗を表示
                logger.debug(f"録音進捗: {i/total_chunks*100:.1f}%")
        logger.info("録音が完了しました")

        stream.stop_stream()
        stream.close()

    def save_recording(self, filename):
        """録音したデータをファイルに保存"""
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        logger.info(f"オーディオを {filename} として保存しました")

    def close(self):
        """PyAudioオブジェクトを終了"""
        self.p.terminate()
        logger.info("オーディオレコーダーを終了しました")

def record_audio(duration=5, output_file="recorded_audio.wav", rate=44100, channels=1):
    """指定された時間だけ音声を録音し、ファイルに保存"""
    recorder = AudioRecorder(rate=rate, channels=channels)
    recorder.start_recording(duration)
    recorder.save_recording(output_file)
    recorder.close()
    return output_file

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="音声録音ツール")
    parser.add_argument("-d", "--duration", type=int, default=10, help="録音時間（秒）")
    parser.add_argument("-o", "--output", default="recorded_audio.wav", help="出力オーディオファイル名")
    parser.add_argument("--rate", type=int, default=44100, help="サンプルレート")
    parser.add_argument("--channels", type=int, default=1, help="チャンネル数")
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
        logger.info(f"出力ディレクトリを作成しました: {output_path.parent}")
    
    logger.info(f"録音を開始します: 時間={args.duration}秒, 出力ファイル={output_path}, サンプルレート={args.rate}, チャンネル数={args.channels}")
    recorded_file = record_audio(duration=args.duration, output_file=str(output_path), rate=args.rate, channels=args.channels)
    logger.success(f"音声を録音し、{recorded_file} として保存しました")