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
        xml_string += (" " + escape(token['token']) + " ")
        xml_string += f'</{token["type"]}>\n'
    xml_string += '</tokens>\n'
    return xml_string

def get_compile_xml(node, level_count=0):
    xml_string = f'<{node["type"]}>'
    if isinstance(node['value'], str):
        xml_string += (" " + escape(node['value']) + " ")
        xml_string += f'</{node["type"]}>'
        return xml_string + '\n'
    else:
        xml_string += '\n'
        for child in node['value']:
            for _ in range(level_count + 1):
                xml_string += '  '
            xml_string += get_compile_xml(child, level_count + 1)
        for _ in range(level_count):
            xml_string += '  '
        xml_string += f'</{node["type"]}>'
        return xml_string + '\n'

def process_file(file_path):
    file = open(file_path, 'r')
    tokens = get_tokens(file.read())
    filename = get_filename(file_path)
    token_output_path = f'{sys.argv[1]}/{filename}T{OUT_FILE_EXTENSION}'
    token_output_file = open(token_output_path, 'w')
    token_xml = get_token_xml(tokens)
    token_output_file.write(token_xml)
    compilation = compile_tokens(tokens)
    compilation_output_path = f'{sys.argv[1]}/{filename}{OUT_FILE_EXTENSION}'
    compilation_output_file = open(compilation_output_path, 'w')
    compile_xml = get_compile_xml(compilation)
    compilation_output_file.write(compile_xml)

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        for dir_filename in os.listdir(sys.argv[1]):
            if not IN_FILE_EXTENSION in dir_filename: continue
            process_file(f'{sys.argv[1]}/{dir_filename}')
    else:
        process_file(sys.argv[1])
