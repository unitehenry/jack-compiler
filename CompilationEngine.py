from TokenNavigator import create, current, advance, previous, peak, has_more_tokens

def is_subroutine_dec(token):
    if token['token'] == 'constructor':
        return True
    if token['token'] == 'function':
        return True
    if token['token'] == 'method':
        return True
    return False

def is_class_var_dec(token):
    if token['token'] == 'static':
        return True
    if token['token'] == 'field':
        return True
    return False

def is_type(token):
    if token['token'] == 'int':
        return True
    if token['token'] == 'char':
        return True
    if token['token'] == 'boolean':
        return True
    if token['type'] == 'identifier':
        return True
    return False

def is_statement(token):
    if token['token'] == 'let':
        return True
    if token['token'] == 'if':
        return True
    if token['token'] == 'while':
        return True
    if token['token'] == 'do':
        return True
    if token['token'] == 'return':
        return True
    return False

def compile_var_dec(navigator):
    node = { 'type': 'varDec', 'value': [] }
    token = current(navigator)
    if token['token'] != 'var':
        raise ValueError('Expected varDec to start with var')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if not is_type(token):
        raise ValueError('Expected subroutine var to have type declaration')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueError('Expected varName to be an identifier')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] == ',':
        while has_more_tokens(navigator):
            token = current(navigator)
            if token['token'] != ',':
                raise ValueError('Expected multiple var names to be followed by ,')
            node['value'].append({
                'type': token['type'],
                'value': token['token']
            })
            token = advance(navigator)
            if token['type'] != 'identifier':
                raise ValueError('Expected varName to be an identifier')
            node['value'].append({
                'type': token['type'],
                'value': token['token']
            })
            token = advance(navigator)
            if token['token'] != ',': break
    token = current(navigator)
    if token['token'] != ';':
        raise ValueError('Expected var declaration to end in ;')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_subroutine_body(navigator):
    node = { 'type': 'subroutineBody', 'value': [] }
    token = advance(navigator)
    if token['token'] != '{':
        raise ValueError('Expected subroutine body definition to start with {')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    while has_more_tokens(navigator):
        token = current(navigator)
        if token['token'] == 'var':
            node['value'].append(compile_var_dec(navigator))
            advance(navigator)
        else:
            break
    node['value'].append(compile_statements(navigator))
    token = current(navigator)
    if token['token'] != '}':
        raise ValueError('Expected subroutineBody to end with }')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_statements(navigator):
    node = { 'type': 'statements', 'value': [] }
    while has_more_tokens(navigator):
        token = current(navigator)
        if is_statement(token):
            node['value'].append(compile_statement(navigator))
            advance(navigator)
        else:
            break
    return node

def compile_statement(navigator):
    token = current(navigator)
    if token['token'] == 'let':
        return compile_let_statement(navigator)
    if token['token'] == 'while':
        return compile_while_statement(navigator)
    if token['token'] == 'do':
        return compile_do_statement(navigator)
    if token['token'] == 'return':
        return compile_return_statement(navigator)
    if token['token'] == 'if':
        return compile_if_statement(navigator)
    raise ValueError(f'Failed to handle statement {token["token"]}')

def compile_if_statement(navigator):
    node = { 'type': 'ifStatement', 'value': [] }
    token = current(navigator)
    if token['token'] != 'if':
        raise ValueError('Expected statement to start with if')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '(':
        raise ValueError('Expected if statement to have (')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_expression(navigator))
    token = advance(navigator)
    if token['token'] != ')':
        raise ValueError('Expected if statement to have )')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '{':
        raise ValueError('Expected if statement to have {')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_statements(navigator))
    token = current(navigator)
    if token['token'] != '}':
        raise ValueError('If statement body should end with }')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = peak(navigator)
    if token['token'] != 'else':
        return node
    token = advance(navigator)
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '{':
        raise ValueError('Expected else statement body to begin with {')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_statements(navigator))
    token = current(navigator)
    if token['token'] != '}':
        raise ValueError('Expected else statement to end with }')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_return_statement(navigator):
    node = { 'type': 'returnStatement', 'value': [] }
    token = current(navigator)
    if token['token'] != 'return':
        raise ValueError('Expected statement to start with return')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != ';':
        node['value'].append(compile_expression(navigator))
        token = advance(navigator)
        if token['token'] != ';':
            raise ValueError('Expected return statement to end with ;')
        return node
    if token['token'] == ';':
        node['value'].append({
            'type': token['type'],
            'value': token['token']
        })
        return node
    raise ValueError('Failed to compile return statement')

def compile_do_statement(navigator):
    node = { 'type': 'doStatement', 'value': [] }
    token = current(navigator)
    if token['token'] != 'do':
        raise ValueError('Expected statement to start with do')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].extend(compile_subroutine_call(navigator))
    token = advance(navigator)
    if token['token'] != ';':
        raise ValueError('Expected do statement to end with ;')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_while_statement(navigator):
    node = { 'type': 'whileStatement', 'value': [] }
    token = current(navigator)
    if token['token'] != 'while':
        raise ValueError('Expected statement to start with while')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '(':
        raise ValueError('While statement should start with (')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_expression(navigator))
    token = advance(navigator)
    if token['token'] != ')':
        raise ValueError('While statement expression should end with )')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '{':
        raise ValueError('While statement body should start with {')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_statements(navigator))
    token = current(navigator)
    if token['token'] != '}':
        raise ValueError('While statement body should end with }')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_let_statement(navigator):
    node = { 'type': 'letStatement', 'value': [] }
    token = current(navigator)
    if token['token'] != 'let':
        raise ValueError('Expected statement to start with let')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueError('Expected statement varName to be indentifier')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] == '=':
        node['value'].append({
            'type': token['type'],
            'value': token['token']
        })
        token = advance(navigator)
        node['value'].append(compile_expression(navigator))
        token = advance(navigator)
        if token['token'] != ';':
            raise ValueError('Expected let statement to end with ;')
        node['value'].append({
            'type': token['type'],
            'value': token['token']
        })
        return node
    if token['token'] != '[':
        raise ValueError('Expected let statement to be followed by [')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_expression(navigator))
    token = advance(navigator)
    if token['token'] != ']':
        raise ValueError('Expected let statement to be followed by ]')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '=':
        raise ValueError('Expected let statement to have =')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    node['value'].append(compile_expression(navigator))
    token = advance(navigator)
    if token['token'] != ';':
        raise ValueError('Expected let statement to end with ;')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_expression(navigator):
    node = { 'type': 'expression', 'value': [] }
    token = current(navigator)
    node['value'].append(compile_term(navigator))
    op_tokens = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    if peak(navigator)['token'] in op_tokens:
        while has_more_tokens(navigator):
            if not peak(navigator)['token'] in op_tokens: break
            token = advance(navigator)
            node['value'].append({ 'type': token['type'], 'value': token['token'] })
            token = advance(navigator)
            node['value'].append(compile_term(navigator))
    return node

def compile_term(navigator):
    node = { 'type': 'term', 'value': [] }
    token = current(navigator)
    if token['type'] in [ 'integerConstant', 'stringConstant' ]:
        node['value'].append({ 'type': token['type'], 'value': token['token'] })
        return node
    if token['token'] in [ 'true', 'false', 'null', 'this' ]:
        node['value'].append({ 'type': 'keywordConstant', 'value': token['token'] })
        return node
    if token['type'] == 'identifier':
        next_token = peak(navigator)
        if next_token['token'] == '(' or next_token['token'] == '.':
            node['value'].extend(compile_subroutine_call(navigator))
            return node
        if next_token['token'] == '[':
            node['value'].append({ 'type': token['type'], 'value': token['token'] })
            token = advance(navigator)
            node['value'].append({ 'type': token['type'], 'value': token['token'] })
            token = advance(navigator)
            node['value'].append(compile_expression(navigator))
            token = advance(navigator)
            if token['token'] != ']':
                raise ValueError('Expected expression to have ]')
            node['value'].append({ 'type': token['type'], 'value': token['token'] })
            return node
        node['value'].append({ 'type': token['type'], 'value': token['token'] })
        return node
    if token['token'] == '(':
        node['value'].append({ 'type': token['type'], 'value': token['token'] })
        token = advance(navigator)
        node['value'].append(compile_expression(navigator))
        token = advance(navigator)
        if token['token'] != ')':
            raise ValueError('Expected expression to have )')
        node['value'].append({ 'type': token['type'], 'value': token['token'] })
        return node
    if token['token'] in [ '-', '~' ]:
        node['value'].append({ 'type': token['type'], 'value': token['token'] })
        token = advance(navigator)
        node['value'].append(compile_term(navigator))
        return node
    raise ValueError(f'Unable to handle term {token["type"]} {token["token"]}')

def compile_subroutine_call(navigator):
    subroutine_nodes = []
    token = current(navigator)
    next_token = peak(navigator)
    if next_token['token'] == '(':
        if token['type'] != 'identifier':
            raise ValueError('Expected subroutineCall to start with identifier')
        subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
        token = advance(navigator)
        if token['token'] != '(':
            raise ValueError('Expected ( in subroutineCall')
        subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
        token = advance(navigator)
        subroutine_nodes.append(compile_expression_list(navigator))
        token = current(navigator)
        if token['token'] != ')':
            raise ValueError('Expected ) in subroutineCall')
        subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
        return subroutine_nodes
    if token['type'] != 'identifier':
        raise ValueError('Expected subroutineCall to start with identifier')
    subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
    token = advance(navigator)
    if token['token'] != '.':
        raise ValueError('Expected subroutineCall to be followed by .')
    subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueError('Expected subroutineCall to be followed with identifier')
    subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
    token = advance(navigator)
    if token['token'] != '(':
        raise ValueError('Expected subroutineCall to be followed by (')
    subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
    token = advance(navigator)
    subroutine_nodes.append(compile_expression_list(navigator))
    token = current(navigator)
    if token['token'] != ')':
        raise ValueError('Expected subroutineCall to be followed by )')
    subroutine_nodes.append({ 'type': token['type'], 'value': token['token'] })
    return subroutine_nodes

def compile_expression_list(navigator):
    node = { 'type': 'expressionList', 'value': [] }
    if current(navigator)['token'] == ')':
        return node
    while has_more_tokens(navigator):
        token = current(navigator)
        if token['token'] == ')': break
        if token['token'] == ',':
            node['value'].append({ 'type': token['type'], 'value': token['token'] })
            token = advance(navigator)
        node['value'].append(compile_expression(navigator))
        advance(navigator)
    return node

def compile_parameter_list(navigator):
    node = { 'type': 'parameterList', 'value': [] }
    token = current(navigator)
    if token['token'] == ')':
        return node
    def compile_param():
        param_nodes = []
        token = current(navigator)
        # param type
        if not is_type(token):
            raise ValueError('Parameter type is not int, char, boolean, class')
        param_nodes.append({
            'type': token['type'],
            'value': token['token']
        })
        token = advance(navigator)
        # param name
        if token['type'] != 'identifier':
            raise ValueError('Parameter name is not an identifier')
        param_nodes.append({
            'type': token['type'],
            'value': token['token']
        })
        token = advance(navigator)
        if token['token'] == ',':
            param_nodes.append({
                'type': token['type'],
                'value': token['token']
            })
            advance(navigator)
            param_nodes.extend(compile_param())
            return param_nodes
        return param_nodes
    node['value'].extend(compile_param())
    return node

def compile_class_var_dec(navigator):
    node = { 'type': 'classVarDec', 'value': [] }
    token = current(navigator)
    if not is_class_var_dec(token):
        raise ValueError('Expected classVarDec to be static or field')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if not is_type(token):
        raise ValueError('Expected classVarDec to have a type')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueErorr('Expected classVarDec varName to be an identifier')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] == ',':
        while has_more_tokens(navigator):
            token = current(navigator)
            if token['token'] != ',':
                raise ValueError('Additional classVarDec varName should be followed by ,')
            node['value'].append({
                'type': token['type'],
                'value': token['token']
            })
            token = advance(navigator)
            if token['type'] != 'identifier':
                raise ValueErorr('Expected classVarDec varName to be an identifier')
            node['value'].append({
                'type': token['type'],
                'value': token['token']
            })
            token = advance(navigator)
            if token['token'] != ',': break
    token = current(navigator)
    if token['token'] != ';':
        raise ValueError('Expected classVarDec to end with ;')
    return node

def compile_subroutine_dec(navigator):
    node = { 'type': 'subroutineDec', 'value': [] }
    token = current(navigator)
    if not is_subroutine_dec(token):
        raise ValueError('Expected constructor, function, or method for subroutine')
    # subroutine return type
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if not (is_type(token) or token['token'] == 'void'):
        raise ValueError('Expected a keyword or identifer for return type')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    # subroutine name
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueError('Expected an identifier for subroutine name')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '(':
        raise ValueError('Subroutine definition requires (')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    advance(navigator)
    node['value'].append(compile_parameter_list(navigator))
    token = current(navigator)
    if token['token'] != ')':
        raise ValueError('Subroutine definition requires )')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    node['value'].append(compile_subroutine_body(navigator))
    return node

def compile_class(navigator):
    node = { 'type': 'class', 'value': [] }
    token = current(navigator)
    if token['token'] != 'class':
        raise ValueError('Expected class keyword')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['type'] != 'identifier':
        raise ValueError('Expected class name identifier')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    token = advance(navigator)
    if token['token'] != '{':
        raise ValueError('Expected to begin class definition with { symbol')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    while has_more_tokens(navigator):
        token = advance(navigator)
        if is_class_var_dec(token):
            node['value'].append(compile_class_var_dec(navigator))
        if is_subroutine_dec(token):
            node['value'].append(compile_subroutine_dec(navigator))
    token = current(navigator)
    if token['token'] != '}':
        raise ValueError('Expected class defintion to end with } symbol')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
    return node

def compile_tokens(tokens):
    navigator = create(tokens)
    return compile_class(navigator)
