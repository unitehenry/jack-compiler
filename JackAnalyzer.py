import sys
import os
from xml.sax.saxutils import escape

from JackTokenizer import get_tokens
from CompilationEngine import compile_tokens

IN_FILE_EXTENSION = '.jack'
OUT_FILE_EXTENSION = '.xml'

def get_filename(file_path):
    return file_path.split('/').pop().split(IN_FILE_EXTENSION)[0]

def get_token_xml(tokens):
    xml_string = '<tokens>\n'
    for token in tokens:
        xml_string += f'<{token["type"]}>'
        xml_string += escape(token['token'])
        xml_string += f'</{token["type"]}>\n'
    xml_string += '</tokens>\n'
    return xml_string

def get_compile_xml(node):
    xml_string = f'<{node["type"]}>'
    if isinstance(node['value'], str):
        xml_string += node['value']
    else:
        for child in node['value']:
            xml_string += get_compile_xml(child)
    xml_string += f'</{node["type"]}>'
    return xml_string + '\n'

def process_file(file_path):
    file = open(file_path, 'r')
    tokens = get_tokens(file.read())
    filename = get_filename(file_path)
    token_output_path = f'{sys.argv[1]}/{filename}T{OUT_FILE_EXTENSION}'
    token_output_file = open(token_output_path, 'w')
    token_output_file.write(get_token_xml(tokens))
    compilation = compile_tokens(tokens)
    compilation_output_path = f'{sys.argv[1]}/{filename}{OUT_FILE_EXTENSION}'
    compilation_output_file = open(compilation_output_path, 'w')
    compilation_output_file.write(get_compile_xml(compilation))

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        for dir_filename in os.listdir(sys.argv[1]):
            if not IN_FILE_EXTENSION in dir_filename: continue
            process_file(f'{sys.argv[1]}/{dir_filename}')
    else:
        process_file(sys.argv[1])
