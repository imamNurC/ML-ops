import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk membaca dan memuat data audio dari folder dataset
def load_data(folder_path):
    data = []
    labels = []

    for label in os.listdir(folder_path):
        label_path = os.path.join(folder_path, label)
        if os.path.isdir(label_path):
            for filename in os.listdir(label_path):
                file_path = os.path.join(label_path, filename)
                if filename.endswith('.wav'):
                    # Membaca audio menggunakan librosa
                    audio_data, sr = librosa.load(file_path, sr=None)
                    
                    # Normalisasi amplitudo
                    audio_data /= np.max(np.abs(audio_data))
                    
                    # Menerapkan windowing
                    window_size = 1024
                    audio_data = librosa.effects.preemphasis(audio_data)
                    audio_data = librosa.effects.preemphasis(audio_data)
                    audio_data = librosa.effects.preemphasis(audio_data)
                    
                    data.append(audio_data)
                    labels.append(label)

    return data, labels, sr

# Path folder dataset
dataset_path = '/path/to/your/dataset'

# Membaca dan memuat data audio
data, labels, sampling_rate = load_data(dataset_path)

# Menampilkan waveform dan spektrogram contoh audio
plt.figure(figsize=(12, 4))
librosa.display.waveshow(data[0], sr=sampling_rate)
plt.title(f'Waveform - Label: {labels[0]}')
plt.show()

plt.figure(figsize=(12, 4))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(data[0]))), sr=sampling_rate, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f'Spectrogram - Label: {labels[0]}')
plt.show()


# ====================================================

import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Fungsi normalisasi sinyal audio
def normalize_audio(audio_signal):
    return audio_signal / np.max(np.abs(audio_signal))

# Fungsi penerapan windowing
def apply_window(audio_signal, window_type='hann'):
    window = librosa.filters.get_window(window_type, len(audio_signal))
    return audio_signal * window

# Contoh fungsi untuk memproses satu file audio
def preprocess_audio(file_path, sampling_rate=44100):
    # Muat audio menggunakan librosa
    audio_signal, _ = librosa.load(file_path, sr=sampling_rate)

    # Normalisasi sinyal audio
    normalized_audio = normalize_audio(audio_signal)

    # Penerapan windowing
    windowed_audio = apply_window(normalized_audio)

    return windowed_audio

# Lokasi folder dataset
dataset_folder = '/path/to/your/dataset/'

# Daftar file audio di folder 'ok/'
ok_files = [os.path.join(dataset_folder, 'ok', file) for file in os.listdir(os.path.join(dataset_folder, 'ok'))]

# Daftar file audio di folder 'ng/'
ng_files = [os.path.join(dataset_folder, 'ng', file) for file in os.listdir(os.path.join(dataset_folder, 'ng'))]

# Contoh penggunaan fungsi preprocess_audio untuk satu file audio 'ok'
ok_example_file = ok_files[0]
preprocessed_ok_audio = preprocess_audio(ok_example_file)

# Tampilkan hasil normalisasi dan windowing
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.title('Original Audio')
plt.plot(np.linspace(0, len(audio_signal) / sampling_rate, len(audio_signal)), audio_signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(1, 2, 2)
plt.title('Preprocessed Audio')
plt.plot(np.linspace(0, len(preprocessed_ok_audio) / sampling_rate, len(preprocessed_ok_audio)), preprocessed_ok_audio)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

# ====================================================

import os
import librosa
import librosa.display
import matplotlib.pyplot as plt

def preprocess_audio(folder_path, label):
    # Membaca file audio dari folder
    audio_files = os.listdir(folder_path)

    # List untuk menyimpan sinyal audio dan label
    audio_data = []
    labels = []

    for file in audio_files:
        # Mendapatkan path lengkap file audio
        file_path = os.path.join(folder_path, file)

        # Membaca sinyal audio menggunakan librosa
        audio, sr = librosa.load(file_path, sr=None)

        # Normalisasi sinyal audio
        normalized_audio = audio / np.max(np.abs(audio))

        # Menyimpan sinyal audio dan label
        audio_data.append(normalized_audio)
        labels.append(label)

    return audio_data, labels

# Mendefinisikan path folder untuk 'ng' dan 'ok'
ng_folder = '/path/to/ng/'
ok_folder = '/path/to/ok/'

# Melakukan preprocessing untuk setiap folder
ng_data, ng_labels = preprocess_audio(ng_folder, label=0)  # Label 0 untuk 'ng'
ok_data, ok_labels = preprocess_audio(ok_folder, label=1)  # Label 1 untuk 'ok'
