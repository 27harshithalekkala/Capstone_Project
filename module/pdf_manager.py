import os

UPLOAD_FOLDER = "uploads"

def save_uploaded_files(uploaded_files):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    saved_files = []

    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.name)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        saved_files.append(file.name)

    return saved_files