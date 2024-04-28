from TokenNavigator import create, current, advance, previous, has_more_tokens

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
    while has_more_tokens(navigator):
        token = advance(navigator)
        if token['token'] == 'var':
            node['value'].append(compile_var_dec(navigator))
        if token['token'] == '}': break
    token = current(navigator)
    if token['token'] != '}':
        return ValueError('Expected subroutineBody to end with }')
    node['value'].append({
        'type': token['type'],
        'value': token['token']
    })
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
