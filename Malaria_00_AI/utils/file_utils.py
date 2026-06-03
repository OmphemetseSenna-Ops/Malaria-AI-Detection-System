import os

def create_directory(path):
    #Create directory if it does not exist
    os.makedirs(path, exist_ok=True)

def get_image_files(image_dir, image_extensions):
    #Get image files and keep best version.Returns dictionary:{base_name: filename}
    images = {}
    for file in os.listdir(image_dir):
        if file.lower().endswith(image_extensions):
            name = os.path.splitext(file)[0]
            if name not in images or file.lower().endswith(".jpg"):
                images[name] = file
    return images


def get_label_files(label_dir):
    # Get all txt label files.
    return [
        file_name
        for file_name in os.listdir(label_dir)
        if file_name.endswith(".txt")
    ]


def get_file_size(path):
    # Return file size.
    return os.path.getsize(path)