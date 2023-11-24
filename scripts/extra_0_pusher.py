import os

# Directory containing the audio files
directory = '../data/raw-data'

# List all files in the directory
files = os.listdir(directory)

# Sort the files to ensure consistent numbering
files.sort()

# Iterate through the files and rename them with track numbers
for i, file in enumerate(files):
    # Check if the file is an audio file (you can add more audio file extensions if needed)
    if file.endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac')):
        
        if file[3] == '_':
            # Create the new file name with the track number
            new_name = f"0{file}"
            # Rename the file
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
        
        

print("0 added at the beginning of 3-digit ID.")