import wave
import numpy as np
import pyaudio
import threading
import joblib
import soundfile as sf
import tkinter as tk
import matplotlib.pyplot as plt
import os
# Load the trained model
model = joblib.load('C:/Users/innovationcenter/Documents/itpkl/nov_model_new.pkl')  # Ganti dengan path sesuai dengan model yang telah dilatih
# Function untuk memproses file audio dan membuat prediksi
def proses_audio():
    # Membaca file audio
    audio_data, sample_rate = sf.read('recorded_audio.wav')
    
    # Meresample jika perlu
    if sample_rate != 44100:
        audio_data = sf.resample(audio_data, 44100)
    
    # Mengubah audio menjadi mono jika perlu
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Normalisasi data audio
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Memisahkan audio menjadi chunk-chunk kecil
    chunk_size = 2048  # Increase chunk_size to match the expected number of features
    num_chunks = len(audio_data) // chunk_size
    chunks = np.array_split(audio_data[:num_chunks * chunk_size], num_chunks)
    
    # Memproses setiap chunk dan membuat prediksi
    for chunk in chunks:
        fft_data = np.abs(np.fft.fft(chunk))[:chunk_size // 2]
        
        # Mengubah format data FFT sesuai dengan model yang dilatih
        input_data = fft_data.reshape(1, -1)  # Karena model membutuhkan input 2D
        
        # Menggunakan model untuk membuat prediksi
        prediction = model.predict(input_data)
    
    if prediction == 0:
        print("Prediksi model: NG")
    else:
        print("Prediksi model: OK")
    
    print("Pemrosesan audio selesai.")

# Function untuk memulai proses rekaman
def start_recording():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording started *")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Recording finished *")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Memproses audio yang direkam
    proses_audio()

    # Menampilkan visualisasi gelombang audio
    audio_data, sample_rate = sf.read('recorded_audio.wav')
    plt.figure(figsize=(10, 4))
    plt.plot(audio_data)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title('Waveform of Recorded Audio')
    plt.show()
    os.remove('recorded_audio.wav')

# Create the UI
root = tk.Tk()
root.title("Audio Recorder")

record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack()

root.mainloop()



#Syarat untuk run dengan mic
