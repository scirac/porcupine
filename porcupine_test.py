
from scipy.signal import resample
import numpy as np
import pyaudio

import pvporcupine
keyword_list = ['hey siri','alexa','ok google']
porcupine = pvporcupine.create(
  access_key='your_key',
  keywords=keyword_list
)

FORMAT = pyaudio.paInt16
CHANNELS = 2
SAMPLED_CHANNELS = 1
ORIGIN_RATE = 48000

frame_length = porcupine.frame_length
SAMPLED_RATE = porcupine.sample_rate
resample_factor = ORIGIN_RATE // SAMPLED_RATE
ORIGIN_CHUNK = frame_length * resample_factor

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=ORIGIN_RATE,
                input=True,
                input_device_index=14,
                )

print('Recording...')
try:
  while True:
    data = stream.read(ORIGIN_CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    audio_data = np.reshape(audio_data, (ORIGIN_CHUNK, CHANNELS))

    channel_one_data = audio_data[:,0]
    num_samples = int(len(channel_one_data) * SAMPLED_RATE / ORIGIN_RATE)
    audio_frame = resample(channel_one_data, num_samples).astype(np.int16)
    keyword_index = porcupine.process(audio_frame)
    if keyword_index in range(len(keyword_list)):
      print(f"{keyword_list[keyword_index]} detected")
except KeyboardInterrupt:
  print("recording stop...")
stream.close()
p.terminate()

porcupine.delete()
