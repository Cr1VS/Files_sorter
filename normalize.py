import re
import os

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
    filename = re.sub(pattern, "_", name.translate(TRANS))
    return filename + ext