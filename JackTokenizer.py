from JackTokens import KEYWORDS, SYMBOLS
import string
import re

def get_token_type(token, terminal):
    if token == '':
        return None
    if token in KEYWORDS:
        return 'keyword'
    if token in SYMBOLS:
        return 'symbol'
    if len(token) >= 3 and token[0] == '"' and token[len(token) - 1] == '"':
        return 'stringConstant'
    if terminal:
        if token.isnumeric() and int(token) >= 0 and int(token) <= 32767:
            return 'integerConstant'
        if not token[0].isnumeric():
            is_identifier = True
            for idx in range(0, len(token)):
                char = token[idx].strip().lower()
                if (not (char in string.ascii_lowercase)) and char != '_':
                    is_identifier = False
            if is_identifier:
                return 'identifier'
    return None

def remove_comments(source_string):
    inline_comment_regex = re.compile('\/\/.+', re.IGNORECASE | re.MULTILINE)
    source_string = re.sub(inline_comment_regex, '', source_string)
    inline_comment_regex = re.compile('\/\*(.)+\*\/', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    source_string = re.sub(inline_comment_regex, '', source_string)
    return source_string

def add_token(tokens, token_type, token_to_add):
    if token_type == 'stringConstant':
        token_to_add = token_to_add[1:len(token_to_add) - 1]
    tokens.append({
        'type': token_type,
        'token': token_to_add
    })

def get_tokens(source_string):
    source_string = remove_comments(source_string)
    tokens = []
    current_token = ''
    for idx in range(0, len(source_string)):
        char = source_string[idx].strip()
        if char == '':
            # in a string constant
            if len(current_token) > 0 and current_token[0] == '"':
                current_token += ' '
                continue
            current_token_type = get_token_type(current_token, True)
            if current_token_type:
                add_token(tokens, current_token_type, current_token)
            current_token = ''
            continue
        char_token_type = get_token_type(char, False)
        if char_token_type == 'symbol':
            current_token_type = get_token_type(current_token, True)
            if current_token_type:
                add_token(tokens, current_token_type, current_token)
            add_token(tokens, char_token_type, char)
            current_token = ''
            continue
        current_token += char
        current_token_type = get_token_type(current_token, False)
        if not current_token_type: continue
        add_token(tokens, current_token_type, current_token)
        current_token = ''
    return tokens
