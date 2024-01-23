import os
from pydub import AudioSegment

def trim_audio(input_file, output_file, start_time_sec, end_time_sec):
    start_time_ms = int(start_time_sec * 1000)
    end_time_ms = int(end_time_sec * 1000)

    audio = AudioSegment.from_wav(input_file)
    trimmed_audio = audio[start_time_ms:end_time_ms]
    trimmed_audio.export(output_file, format="wav")

def main():
    input_folder = "ini/folder/asal"
    output_folder = "hasil"

    # Membuat folder output jika belum ada
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    # Mendapatkan list file dalam folder input
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]

    for audio_file in audio_files:
        input_file_path = os.path.join(input_folder, audio_file)
        output_file_path = os.path.join(output_folder, audio_file)

        start_time = float(input(f"Masukkan start time untuk {audio_file} (dalam detik): "))
        end_time = float(input(f"Masukkan end time untuk {audio_file} (dalam detik): "))

        # Membuat nama file output dengan folder yang sama
        output_folder_path = os.path.join(output_folder, audio_file)
        trim_audio(input_file_path, output_folder_path, start_time, end_time)
        print(f"{audio_file} telah dipotong dan disimpan di {output_folder}")

if __name__ == "__main__":
    main()
