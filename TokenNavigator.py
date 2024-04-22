def create(tokens):
    return {
        'idx': 0,
        'tokens': tokens
    }

def current(navigator):
    return navigator['tokens'][navigator['idx']]

def advance(navigator):
    navigator['idx'] += 1
    return navigator['tokens'][navigator['idx']]

def previous(navigator):
    navigator['idx'] -= 1
    return navigator['tokens'][navigator['idx']]

def has_more_tokens(navigator):
    token_length = len(navigator['tokens'])
    return navigator['idx'] < (token_length - 1)
