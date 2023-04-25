import os
import re
import math
import shutil
import openai
from glob import glob
from dotenv import load_dotenv
from pydub import AudioSegment

class AudioTranscribe:
    def __init__(self, audio_path):
        load_dotenv()
        openai.api_key = os.environ['OPENAI_API_KEY']
        self.audio_path = audio_path

    def chunk(self):
        audio = AudioSegment.from_file(self.audio_path, format='mp3')
        os.mkdir('chunks')
        chunk_size = 20000000
        chunk_duration = math.floor(chunk_size / audio.frame_rate * 1000)

        for i, chunk_start in enumerate(range(0, len(audio), chunk_duration)):
            chunk_end = chunk_start + chunk_duration
            if chunk_end > len(audio):
                chunk_end = len(audio)
            chunk_ = audio[chunk_start:chunk_end]
            chunk_.export(f'chunks/audio_chunk_{i}.mp3', format='mp3')

    def get_transcribe(self, path):
        audio_file = open(path, 'rb')
        transcript = openai.Audio.transcribe('whisper-1', audio_file)
        return transcript['text']

    def extract_number(self, name):
        return int(re.search(r"\d+", name).group())
    
    def transcribe(self):
        self.chunk()
        lista_audio = glob('chunks/*.mp3')
        lista_audio = sorted(lista_audio, key=self.extract_number)
        transcript = list(map(self.get_transcribe, lista_audio))
        transcript = ' '.join(transcript)
        shutil.rmtree('chunks', ignore_errors=True)
        return transcript
