import argparse

from audio_transcribe.gpt import QuestionBot
from audio_transcribe.whisper import AudioTranscribe

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Input an mp3 file path and ask questions " "about its content to ChatGPT"
        )
    )
    parser.add_argument("-path", required=True, help="Path to the mp3 file")
    args = parser.parse_args()
    audio_transcribe = AudioTranscribe(args.path)
    print("Getting Transcript...")
    transcript = audio_transcribe.transcribe()
    print(
        "Preprocessing finished. Ask questions about the audio content."
        ' Write "exit" to quit.'
    )
    bot = QuestionBot(transcript)
    bot.chat()
