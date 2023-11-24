import os

def list_files(directory):
    file_names = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_names.append(filename)
    return file_names

# Replace 'your_directory_path' with the path to the directory you want to explore
directory_path = '../data/raw-data/'

file_names = list_files(directory_path)

file_names_output_path = '../data/raw-data-file-name.txt'


with open(file_names_output_path, 'w') as file:
    for name in sorted(file_names):
        file.write(name + '\n')

print(f"File names saved to {file_names_output_path}")