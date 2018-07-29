import os
import subprocess

lib_dir = os.path.join(os.path.dirname(__file__), 'lib')
picoTTS = os.path.join(lib_dir, 'picoTTS')


def readText(text):
    subprocess.call([picoTTS, text])
