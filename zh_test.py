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
CHANNELS = 1
frame_length = porcupine.frame_length
SAMPLE_RATE = porcupine.sample_rate
CHUNK = frame_length

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True
                )

print('Recording...')
try:
  while True:
    data = stream.read(CHUNK)
    audio_frame = np.frombuffer(data, dtype=np.int16)
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
