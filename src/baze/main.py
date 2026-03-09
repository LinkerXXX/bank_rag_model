import os
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from docling_parser.parser import parser_pdf
from ollama_model.model import ollama_embed
from qdrant_bd.upload import qdrant_upload
from docling_parser.chanking import recursive_chunk

data_dir = 'data'
filename = 'test.pdf'

# 1 шаг - распарсили в строку и записали в файл тхт
result = parser_pdf('data/test.pdf')
file = open("data/parse.txt", "w")
file.write(result)
file.close()

# 2 шаг - чанкуем
result_ch = recursive_chunk(result, 500, 0)

# 3 шаг - отдали результат модели на векторизацию
# model = 'mxbai-embed-large'
# promt = 'data'
vector = ollama_embed('mxbai-embed-large', result_ch)

# шаг 4 загрузили в бд
qdrant_upload('localhost', 6333, 'test', 1024)


# рекурсивно разрезали текст(хз как, надо смотреть еще раз)
# надо разобраться как это грузится в бд