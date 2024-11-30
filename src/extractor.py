import os

try:
    import magic
    import zipfile

    ALLOW_EXTRACTION = True
except ImportError:
    ALLOW_EXTRACTION = False

try:
    import py7zr

    ALLOW_7ZIP = True
except ImportError:
    ALLOW_7ZIP = False


def extract_file(zip_file):
    """
    Detects the file type and extracts the data accordingly.
    """

    if not ALLOW_EXTRACTION:
        exit("magic is required to extract files.")

    file_type = magic.from_file(zip_file, mime=True)

    path, filename = os.path.split(zip_file)
    filename, ext = os.path.splitext(filename)

    extract_directory = str(os.path.join(path, filename))

    if not os.path.exists(extract_directory):
        os.makedirs(extract_directory)

    print(f"Attempting to extract {filename}...")

    if file_type == "application/x-7z-compressed":
        if not ALLOW_7ZIP:
            exit("py7zr is required to extract .7z files.")

        with py7zr.SevenZipFile(zip_file, "r") as z:
            z.extractall(extract_directory)

    elif file_type == "application/zip":
        with zipfile.ZipFile(zip_file, "r") as z:
            z.extractall(extract_directory)

    else:
        exit(f"Unsupported type: `{file_type}`")

    os.remove(zip_file)

    print(f"Files extracted to '{extract_directory}'.")
