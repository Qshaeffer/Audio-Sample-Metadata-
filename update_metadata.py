# searches folder(s) for file names matching those in reference CSV, then writes corresponding metadata to FLAC file

import csv
import os
from mutagen.flac import FLAC

# Full path to your CSV file
csv_file = r'C:\Users\Quentin\Documents\CSV\sample_descriptions.csv'

# Master directory containing your FLAC audio files and subfolders
master_directory = r'C:\Users\Quentin\MusicProduction\FLACSamples'

# Create a dictionary to store sample names and descriptions
sample_dict = {}

# Read your data from the CSV file
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row if it exists
    for row in reader:
        sample_name, description = row
        sample_dict[sample_name] = description

# Function to update FLAC metadata
def update_flac_metadata(filepath, description):
    audio = FLAC(filepath)
    
    # Update the description field (or change to 'comment' if preferred)
    audio['description'] = description
    
    audio.save()
    print(f"Updated metadata for {os.path.basename(filepath)}")

# Walk through all subdirectories
for root, dirs, files in os.walk(master_directory):
    for file in files:
        if file.lower().endswith('.flac'):
            filename_without_extension = os.path.splitext(file)[0]  # Remove file extension
            if filename_without_extension in sample_dict:
                try:
                    update_flac_metadata(os.path.join(root, file), sample_dict[filename_without_extension])
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
            else:
                print(f"No description found for {filename_without_extension}")

print("Finished processing files.")
