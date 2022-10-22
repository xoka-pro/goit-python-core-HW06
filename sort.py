import re
import shutil
import sys
from pathlib import Path

# === ГЛОБАЛЬНІ ЗМІННІ ===
target_folders = ['images', 'documents', 'audio', 'video', 'archives', ]

# списки файлів у кожній категорії
image_files = []
document_files = []
audio_files = []
video_files = []
archive_files = []

known_ext = []  # перелік усіх відомих розширень
unknown_ext = []  # перелік НЕ відомих розширень
# === КІНЕЦЬ ГЛОБАЛЬНИХ ЗМІННИХ ===


def init(folder: Path) -> None:
    """ функція створює цільові директорії"""

    for element in target_folders:
        new_folder = folder / element
        new_folder.mkdir(exist_ok=True, parents=True)
    return None


def cleaner(folder: Path) -> None:
    """функція рекурсивно видаляє порожні директорії в робочій директорії виключаючі цільові"""
    for element in folder.iterdir():
        if element.is_dir():
            if element.name not in target_folders:
                cleaner(element)
                try:
                    element.rmdir()
                except:
                    print(f'Directory {element} is not empty. Can not remove')
                    continue
    return None


def normalize(filename) -> str:
    """  Функція normalize:

    +++ 1. Проводить транслітерацію кирилічного алфавіту на латинський.
    +++ 2. Замінює всі символи крім латинських літер, цифр на '_'.

    Вимоги до функції normalize:
    +++ приймає на вхід рядок та повертає рядок;
    +++ проводить транслітерацію кирилічних символів на латиницю;
    +++ замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
    +++ транслітерація може не відповідати стандарту, але бути читабельною;
    +++ великі літери залишаються великими, а маленькі — маленькими після транслітерації.  """

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyr)] = lat
        TRANS[ord(cyr.upper())] = lat.upper()

    transcripted_filename = filename.translate(TRANS)

    normalized_filename = re.sub('[^A-Za-z0-9.]+', '_', transcripted_filename)

    return normalized_filename


def read_folder(path: Path) -> None:
    """ функція рекурсивно обходе всі підпапки та минає цільові директорії"""
    for element in path.iterdir():
        if element.is_dir() and element not in target_folders:
            read_folder(element)
        else:
            sort_folder(element)
    return None


def archive_handler(file: Path) -> None:

    folder_for_file = Path(normalize(file.name.replace(file.suffix, '')))
    folder_for_file.mkdir(exist_ok=True, parents=True)

    try:
        shutil.unpack_archive(str(file.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Це не архів {file}!')
        folder_for_file.rmdir()
    return None


def sort_folder(folder: Path) -> None:
    """
    функція:
    - переносе файли по директоріях за шаблонами
    - заповнює списки файлів
    - заповнює списки відомих та невідомих розширень
    """

    # визначаємо розширення за якими будемо сортувати файли
    image_ext = ['JPEG', 'PNG', 'JPG', 'SVG', ]
    document_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', ]
    audio_ext = ['MP3', 'OGG', 'WAV', 'AMR', ]
    video_ext = ['AVI', 'MP4', 'MOV', 'MKV', ]
    archive_ext = ['ZIP', 'GZ', 'TAR', ]

    for file in folder.iterdir():
        if file.suffix[1:].upper() in image_ext:
            image_folder = Path('images')
            file.replace(folder / image_folder / normalize(file.name))
            known_ext.append(file.suffix)
            image_files.append(file.name)

        elif file.suffix[1:].upper() in document_ext:
            document_folder = Path('documents')
            file.replace(folder / document_folder / normalize(file.name))
            known_ext.append(file.suffix)
            document_files.append(file.name)

        elif file.suffix[1:].upper() in audio_ext:
            audio_folder = Path('audio')
            file.replace(folder / audio_folder / normalize(file.name))
            known_ext.append(file.suffix)
            audio_files.append(file.name)

        elif file.suffix[1:].upper() in video_ext:
            video_folder = Path('video')
            file.replace(folder / video_folder / normalize(file.name))
            known_ext.append(file.suffix)
            video_files.append(file.name)

        elif file.suffix[1:].upper() in archive_ext:
            archive_folder = Path('archives')
            new_archive = folder / archive_folder / normalize(file.name)
            file.replace(new_archive)
            archive_handler(new_archive)
            known_ext.append(file.suffix)
            archive_files.append(file.name)

        else:
            # file.suffix[1:].upper() not in image_ext and document_ext and audio_ext and video_ext and archive_ext:
            normalize(file.name)
            if not file.is_dir():
                unknown_ext.append(file.suffix)

    return None


if __name__ == '__main__':

    # if len(sys.argv) < 2:
    #     print(f'The path to folder is not specified. Check arguments.')
    #     exit()
    # folder_to_clean = sys.argv[1]
    # if not Path(folder_to_clean).is_dir():
    #     print(f'Your argument is not folder. Check arguments.')
    #     exit()

    output_folder = Path('test')
    init(output_folder)
    read_folder(output_folder)
    cleaner(output_folder)

    print(f'Відомі розширення файлів: {known_ext}')
    print(f'Невідомі розширення файлів: {unknown_ext}')
    print(f'Список файлів у категорії "зображення": {image_files}')
    print(f'Список файлів у категорії "документи": {document_files}')
    print(f'Список файлів у категорії "музика": {audio_files}')
    print(f'Список файлів у категорії "відео": {video_files}')
    print(f'Список файлів у категорії "архіви": {archive_files}')
