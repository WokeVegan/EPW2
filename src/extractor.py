import enum
import os
import zipfile

try:
    import py7zr

    ALLOW_7ZIP = True
except ImportError:
    ALLOW_7ZIP = False

try:
    import patoolib

    ALLOW_RAR = True
except ImportError:
    ALLOW_RAR = False


class FileType(enum.Enum):
    UNKNOWN = enum.auto()
    ZIP = enum.auto()
    SEVEN_ZIP = enum.auto()
    RAR = enum.auto()
    RAR5PLUS = enum.auto()


def get_file_type(filename) -> FileType:
    file_signatures = {
        FileType.SEVEN_ZIP: bytes([0x37, 0x7A, 0xBC, 0xAF, 0x27, 0x1C]),
        FileType.ZIP: bytes([0x50, 0x4B, 0x03, 0x04]),
        FileType.RAR5PLUS: bytes([0x52, 0x61, 0x72, 0x21, 0x1A, 0x07, 0x01, 0x00]),
        FileType.RAR: bytes([0x52, 0x61, 0x72, 0x21, 0x1A, 0x07, 0x00]),
    }

    read_size = max([len(x) for x in file_signatures.values()])

    with open(filename, "rb") as f:
        head = f.read(read_size)

        for file_type, signature in file_signatures.items():
            if head.startswith(signature):
                return file_type

    return FileType.UNKNOWN


def extract_file(zip_file, add_to_new_folder=False, delete_archive=True):
    """
    Detects the file type and extracts the data accordingly.
    """

    path, filename = os.path.split(zip_file)
    filename, ext = os.path.splitext(filename)

    if add_to_new_folder:
        extract_directory = str(os.path.join(path, filename))
    else:
        extract_directory = path

    if not os.path.exists(extract_directory):
        os.makedirs(extract_directory)

    print(f"Attempting to extract {filename}...")

    file_type = get_file_type(zip_file)

    if file_type == FileType.SEVEN_ZIP:
        if not ALLOW_7ZIP:
            exit("py7zr is required to extract .7z files.")

        with py7zr.SevenZipFile(zip_file, "r") as z:
            z.extractall(extract_directory)

    elif file_type == FileType.ZIP:
        with zipfile.ZipFile(zip_file, "r") as z:
            z.extractall(extract_directory)
    elif file_type in [FileType.RAR, FileType.RAR5PLUS]:
        if not ALLOW_RAR:
            exit("rarfile is required to extract .rar files.")
        try:
            patoolib.extract_archive(zip_file, extract_directory)
        except BaseException:
            print("Failed to extract rar file.")
            delete_archive = False
    else:
        exit(f"Unsupported type: `{file_type}`")

    if delete_archive:
        os.remove(zip_file)

    print(f"Files extracted to '{extract_directory}'.")
