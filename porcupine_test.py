
from scipy.signal import resample
import numpy as np
import pyaudio

import pvporcupine
keyword_list = ['hey siri','alexa','ok google']
porcupine = pvporcupine.create(
  access_key='your key',
  keywords=keyword_list
)

FORMAT = pyaudio.paInt16
CHANNELS = 1
frame_length = porcupine.frame_length
SAMPLE_RATE = porcupine.sample_rate
CHUNK = frame_length

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                )

print('Recording...')
try:
  while True:
    data = stream.read(CHUNK)
    audio_frame = np.frombuffer(data, dtype=np.int16)
    keyword_index = porcupine.process(audio_frame)
    if keyword_index in range(len(keyword_list)):
      print(f"{keyword_list[keyword_index]} detected")
except KeyboardInterrupt:
  print("recording stop...")
finally:
    stream.close()
    p.terminate()

    porcupine.delete()
