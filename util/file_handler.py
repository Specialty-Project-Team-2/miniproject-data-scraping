def make_file_path(filename):
    return f"./data/{filename}"

def saveAsFile(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def saveAsFileWithGenerator(file_path, iterable_content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(iterable_content)
        
def load_file(file_path):
    result = None
    with open(f"./data/{file_path}", "r", encoding="utf-8") as file:
        result = file.read()
    return result