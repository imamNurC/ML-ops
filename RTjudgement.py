import numpy as np
import pyaudio
import wave
import joblib
import librosa
import tkinter as tk

# Load the model
MODEL_PATH = 'C:/Users/ITPKL/Desktop/pydev/model20240130.pkl'
model = joblib.load(MODEL_PATH)

# Define a function to record audio from microphone and save as WAV file
def record_audio(file_path, duration=5, sample_rate=44100, channels=1, format=pyaudio.paInt16):
    chunk = 1024
    audio_format = format
    p = pyaudio.PyAudio()
    
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    frames = []
    print("Recording...")
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to process recorded audio file
def process_recorded_audio(file_path):
    # Load the recorded audio file
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    
    # Convert stereo to mono if needed
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Normalize the audio data
    audio_data /= np.max(np.abs(audio_data))
    
    # Perform any additional processing needed, e.g., feature extraction
    
    # Make prediction
    scaled_input = audio_data.reshape(1, -1)  # Reshape for compatibility with scaler
    y_pred = model.predict(scaled_input)
    
    # Print prediction
    print("Prediction:", "NG" if y_pred == 0 else "OK")

# Function to start recording and process the recorded audio
def start_recording_and_process():
    # Define file path to save recorded audio
    file_path = 'recorded_audio.wav'
    
    # Record audio
    record_audio(file_path)
    
    # Process recorded audio
    process_recorded_audio(file_path)

# Create a tkinter window
window = tk.Tk()
window.title("Real-time Audio Prediction")
window.geometry("300x100")

# Create a button to start recording and processing
record_button = tk.Button(window, text="Start Recording", command=start_recording_and_process)
record_button.pack()

window.mainloop()
