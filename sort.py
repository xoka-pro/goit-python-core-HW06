import re
import shutil


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


def sort_folder(folder):
    """
    - зображення ('JPEG', 'PNG', 'JPG', 'SVG') переносимо до папки images
    - документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX') переносимо до папки documents
    - аудіо файли ('MP3', 'OGG', 'WAV', 'AMR') переносимо до audio
    - відео ('AVI', 'MP4', 'MOV', 'MKV') файли до video
    - архіви ('ZIP', 'GZ', 'TAR') розпаковуються та їх вміст переноситься до папки archives

    !!!
    Щоб скрипт міг пройти на будь-яку глибину вкладеності,
    функція обробки папок повинна рекурсивно викликати сама себе, коли їй зустрічаються вкладенні папки.


    """

    # визначаємо розширення за якими будемо сортувати файли
    image_ext = ['JPEG', 'PNG', 'JPG', 'SVG', ]
    document_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', ]
    audio_ext = ['MP3', 'OGG', 'WAV', 'AMR', ]
    video_ext = ['AVI', 'MP4', 'MOV', 'MKV', ]
    archive_ext = ['ZIP', 'GZ', 'TAR', ]

    # списки файлів у кожній категорії
    image_files = []
    document_files = []
    audio_files = []
    video_files = []
    archive_files = []

    known_ext = []  # перелік усіх відомих розширень
    unknown_ext = []  # перелік НЕ відомих розширень

    ignore_folders = ['images', 'documents', 'audio', 'video', 'archives', ]

    pass


if __name__ == '__main__':
    print(normalize('ТеСтОвИй ТЕКСТ іїє 12345 <>@#$"".jpg'))
