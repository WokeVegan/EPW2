import os

try:
    import magic
    import zipfile

    ALLOW_EXTRACTION = True
except ImportError:
    ALLOW_EXTRACTION = False

try:
    import pyunpack

    ALLOW_7ZIP = True
except ImportError:
    ALLOW_7ZIP = False


def extract_file(zip_file):
    """
    Detects the file type and extracts the data accordingly.
    """

    # Quit if magic isn't installed
    if not ALLOW_EXTRACTION:
        exit("magic is required to extract files.")

    # Use magic to get the file signature
    file_type = magic.from_file(zip_file, mime=True)

    path, filename = os.path.split(zip_file)
    filename, ext = os.path.splitext(filename)

    extract_directory = os.path.join(path, filename)

    if not os.path.exists(extract_directory):
        os.makedirs(extract_directory)

    if file_type == "application/x-7z-compressed":
        # Exit if pyunpack isn't installed
        if not ALLOW_7ZIP:
            exit("pyunpack and patool are required to extract 7z files.")

        pyunpack.Archive(zip_file).extractall(extract_directory)

    elif file_type == "application/zip":
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(extract_directory)

    else:
        exit(f"Unsupported type: `{file_type}`")

    # remove the zip file after extracting
    os.remove(zip_file)

    print(f"Files extracted to '{extract_directory}'.")
