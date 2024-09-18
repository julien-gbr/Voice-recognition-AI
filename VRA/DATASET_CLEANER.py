import os
import shutil
import librosa
import soundfile as sf

input_directory = "Recording_files"
output_directory = "Clean_files"
target_sample_rate = 16000

def process_audio_file(input_file_path, output_file_path):
    # Get the audio file
    y, sr = librosa.load(input_file_path, sr=None)

    # Delete silence moments at the beginning and the end
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)

    # Then change the frequency
    y_resampled = librosa.resample(y_trimmed, orig_sr=sr, target_sr=target_sample_rate)

    # Then save the new file
    sf.write(output_file_path, y_resampled, target_sample_rate)

# This is the function to parse all the files and to store them in the new directory
def file_parser(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        recording_files_path = os.path.relpath(root, input_dir)
        new_folder = os.path.join(output_dir, recording_files_path)

        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        for file in files:
            if file.lower().endswith('.wav'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(new_folder, file)

                print(f"Start analysing: {input_file_path}")

                process_audio_file(input_file_path, output_file_path)
            else:
                print(f"The file remains the same: {input_file_path}. Check why.")
                shutil.copy2(os.path.join(root, file), os.path.join(new_folder, file))

file_parser(input_directory, output_directory)
