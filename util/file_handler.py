def make_file_path(filename):
    return f"./data/{filename}"

def saveAsFile(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)