import os
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from docling_parser.parser import parser_pdf

data_dir = 'data'
filename = 'test.pdf'

result = parser_pdf('data/test.pdf')

file = open("data/parse.txt", "w")

file.write(result)

file.close()
