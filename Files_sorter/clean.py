import re
import os
from pathlib import Path
import shutil
import sys

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCS = []
DOCX_DOCS = []
TXT_DOCS = []
PDF_DOCS = []
XLSX_DOCS = []
PPTX_DOCS = []
ARCHIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "JPG": JPG_IMAGES,
    "PNG": PNG_IMAGES,
    "SVG": SVG_IMAGES,
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCS,
    "DOCX": DOCX_DOCS,
    "TXT": TXT_DOCS,
    "PDF": PDF_DOCS,
    "XLSX": XLSX_DOCS,
    "PPTX": PPTX_DOCS,
    "ZIP": ARCHIVES,
    "GZ": ARCHIVES,
    "TAR": ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():       
        if item.is_dir():
            if item.name not in ("archives", "video", "audio", "documents", "images", "MY_OTHER"):
                FOLDERS.append(item)
                scan(item)
            continue
        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension].append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)
                

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "yo", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "kh", "ts", "ch", "sh", "shch", "'", "y", "'", "e", "yu", "ya", "ye", "i", "yi", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

pattern = r"\W"

def normalize(name: str) -> str:
    filename, ext = os.path.splitext(name)
    filename = re.sub(pattern, "_", filename.translate(TRANS))
    return filename + ext  


def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / "images" / "JPEG")
    for file in JPG_IMAGES:
        handle_media(file, folder / "images" / "JPG")
    for file in PNG_IMAGES:
        handle_media(file, folder / "images" / "PNG")
    for file in SVG_IMAGES:
        handle_media(file, folder / "images" / "SVG")
    for file in MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3_AUDIO")
    for file in OGG_AUDIO:
        handle_media(file, folder / "audio" / "OGG_AUDIO")
    for file in WAV_AUDIO:
        handle_media(file, folder / "audio" / "WAV_AUDIO")
    for file in AMR_AUDIO:
        handle_media(file, folder / "audio" / "AMR_AUDIO")
    for file in DOC_DOCS:
        handle_media(file, folder / "documents" / "DOC_DOCS")
    for file in DOCX_DOCS:
        handle_media(file, folder / "documents" / "DOCX_DOCS")
    for file in TXT_DOCS:
        handle_media(file, folder / "documents" / "TXT_DOCS")
    for file in PDF_DOCS:
        handle_media(file, folder / "documents" / "PDF_DOCS")
    for file in XLSX_DOCS:
        handle_media(file, folder / "documents" / "XLSX_DOCS")
    for file in PPTX_DOCS:
        handle_media(file, folder / "documents" / "PPTX_DOCS")
    for file in AVI_VIDEO:
        handle_media(file, folder / "video" / "AVI")
    for file in MP4_VIDEO:
        handle_media(file, folder / "video" / "MP4")
    for file in MOV_VIDEO:
        handle_media(file, folder / "video" / "MOV")
    for file in MKV_VIDEO:
        handle_media(file, folder / "video" / "MKV")    
    for file in MY_OTHER:
        handle_media(file, folder / "MY_OTHER")

    for file in ARCHIVES:
        handle_archive(file, folder / "ARCHIVES")

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f"Error during remove folder {folder}")


def run():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)