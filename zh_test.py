
from scipy.signal import resample
import numpy as np
import pyaudio
import wave
import pvporcupine

wf = wave.open('./response_word/response.wav','rb')

write_p = pyaudio.PyAudio()
write_stream = write_p.open(format = pyaudio.paInt16,
                            channels= wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True
)
response_audio = wf.readframes(wf.getnframes())

porcupine = pvporcupine.create(
  access_key='your key',
  keyword_paths=['./keyword/小勤_zh_windows_v3_0_0.ppn'],
  model_path='./model/porcupine_params_zh.pv'
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
    if keyword_index == 0:
        print("小勤 detected")
        write_stream.write(response_audio)

except KeyboardInterrupt:
  print("recording stop...")
finally:
    stream.close()
    p.terminate()
    write_stream.close()
    write_p.terminate()
    wf.close()
    porcupine.delete()
