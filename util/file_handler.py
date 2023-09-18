import os
import json


def make_file_path(filename):
    return f"./data/{filename}"

def saveAsFile(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def saveAsJson(file_path, dictionary):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(dictionary, file, ensure_ascii=False)

def saveAsFileWithGenerator(file_path, iterable_content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(iterable_content)
        
def load_file(file_path):
    result = None
    with open(make_file_path(file_path), "r", encoding="utf-8") as file:
        result = file.read()
    return result

def load_json(file_path):
    result = None
    with open(make_file_path(file_path), "r", encoding="utf-8") as file:
        result = json.load(file)
    return result

def load_file_line_by_line(file_path):
    with open(make_file_path(file_path), "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def iterator_dir_children(dir_path):
    full_dir_path = make_file_path(dir_path)
    try:
        for file in os.listdir(full_dir_path):
            file_path = os.path.join(full_dir_path, file)
            if not os.path.isfile(file_path): continue
            
            yield os.path.join(dir_path, file)
            
    except OSError as e:
        print(f"Error reading directory: {e}")