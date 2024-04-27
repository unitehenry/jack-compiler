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
    if token['token'] == '}':
        return node
    def compile_var():
        var_nodes = []
        token = current(navigator)
        if token['token'] != 'var':
            return param_nodes
        var_nodes.append({
            'type': token['type'],
            'value': token['token']
        })
        token = advance(navigator)
        if not is_type(token):
            raise ValueError('Expected subroutine var to have type declaration')
        var_nodes.append({
            'type': token['type'],
            'value': token['token']
        })
        def compile_varname():
            varname_nodes = []
            token = advance(navigator)
            if token['type'] != 'identifier':
                raise ValueError('Expected varName to be an identifier')
            varname_nodes.append({
                'type': token['type'],
                'value': token['token']
            })
            token = advance(navigator)
            if token['token'] != ',':
                return varname_nodes
            varname_nodes.append({
                'type': token['type'],
                'value': token['token']
            })
            varname_nodes.extend(compile_varname())
            return varname_nodes
        var_nodes.extend(compile_varname())
        token = current(navigator)
        if token['token'] != ';':
            raise ValueError('Expected varDec to end with ;')
        var_nodes.append({
          'type': token['type'],
          'value': token['token']
        })
        token = advance(navigator)
        if token['token'] == 'var':
            var_nodes.extend(compile_var())
            return var_nodes
        return var_nodes
    node['value'].extend(compile_var())
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
    return None

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
