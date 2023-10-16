from pathlib import Path
import shutil
import sys
import files_parser
from normalize import normalize

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
    files_parser.scan(folder)
    for file in files_parser.JPEG_IMAGES:
        handle_media(file, folder / "images" / "JPEG")
    for file in files_parser.JPG_IMAGES:
        handle_media(file, folder / "images" / "JPG")
    for file in files_parser.PNG_IMAGES:
        handle_media(file, folder / "images" / "PNG")
    for file in files_parser.SVG_IMAGES:
        handle_media(file, folder / "images" / "SVG")
    for file in files_parser.MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3_AUDIO")
    for file in files_parser.OGG_AUDIO:
        handle_media(file, folder / "audio" / "OGG_AUDIO")
    for file in files_parser.WAV_AUDIO:
        handle_media(file, folder / "audio" / "WAV_AUDIO")
    for file in files_parser.AMR_AUDIO:
        handle_media(file, folder / "audio" / "AMR_AUDIO")
    for file in files_parser.DOC_DOCS:
        handle_media(file, folder / "documents" / "DOC_DOCS")
    for file in files_parser.DOCX_DOCS:
        handle_media(file, folder / "documents" / "DOCX_DOCS")
    for file in files_parser.TXT_DOCS:
        handle_media(file, folder / "documents" / "TXT_DOCS")
    for file in files_parser.PDF_DOCS:
        handle_media(file, folder / "documents" / "PDF_DOCS")
    for file in files_parser.XLSX_DOCS:
        handle_media(file, folder / "documents" / "XLSX_DOCS")
    for file in files_parser.PPTX_DOCS:
        handle_media(file, folder / "documents" / "PPTX_DOCS")
    for file in files_parser.AVI_VIDEO:
        handle_media(file, folder / "video" / "AVI")
    for file in files_parser.MP4_VIDEO:
        handle_media(file, folder / "video" / "MP4")
    for file in files_parser.MOV_VIDEO:
        handle_media(file, folder / "video" / "MOV")
    for file in files_parser.MKV_VIDEO:
        handle_media(file, folder / "video" / "MKV")    
    for file in files_parser.MY_OTHER:
        handle_media(file, folder / "MY_OTHER")

    for file in files_parser.ARCHIVES:
        handle_archive(file, folder / "ARCHIVES")

    for folder in files_parser.FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f"Error during remove folder {folder}")


if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())