# converters various audio file types to FLAC

import os
from pydub import AudioSegment
from tqdm import tqdm

# Define paths
input_directory = r'C:\your\sample\library'
output_directory = r'C:\your\new\flac\library'
supported_formats = ('.wav', '.mp3', '.ogg', '.aiff', '.flv', '.mp4', '.wma')

# set compression levels 0-8
def convert_to_flac(input_path, output_path):
    try:
        print(f"Converting {input_path} to {output_path}")  # Debug info
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format='flac', parameters=["-compression_level", "6"])
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        return False

# Walk through input directory and process files
total_files = sum(len(files) for _, _, files in os.walk(input_directory))
with tqdm(total=total_files, desc="Processing files") as pbar:
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                input_file_path = os.path.join(root, file)

                # Determine the corresponding output path
                relative_path = os.path.relpath(root, input_directory)
                output_dir = os.path.join(output_directory, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.flac')

                # Convert to FLAC and save in the output directory
                if convert_to_flac(input_file_path, output_file_path):
                    print(f"Converted {input_file_path} to {output_file_path}")
                else:
                    print(f"Failed to convert {input_file_path}")

            pbar.update(1)

print("Processing completed successfully!")
