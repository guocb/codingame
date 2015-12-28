import sys
import math


TOK_STR = 0
TOK_VAR = 1
TOK_EQ = 2
TOK_SEMI = 3
TOK_LP = 4
TOK_RP = 5

def get_tokens(text):
    ci = iter(text)
    c = next(ci)
    while True:
        if c in [' ', '\t', '\n']:
            c = next(ci)
            continue
        if c == "'":
            value = "'"
            c = next(ci)
            while c != "'":
                value += c
                c = next(ci)
            value += "'"
            yield (TOK_STR, value)
            c = next(ci)
        if c.isalnum():
            value = c
            c = next(ci)
            while c.isalnum():
                value += c
                c = next(ci)
            yield (TOK_VAR, value)
        if c == '=':
            yield (TOK_EQ, '=')
            c = next(ci)
        if c == ';':
            yield (TOK_SEMI, ';')
            c = next(ci)
        if c == '(':
            yield (TOK_LP, '(')
            c = next(ci)
        if c == ')':
            yield (TOK_RP, ')')
            c = next(ci)
                

class Formatter(object):
    def __init__(self):
        self.indent = 0
        self.stream = ''
        
    def add_token(self, tok, newline=False):
        if newline:
            self.stream += '\n' + ' ' * 4 * self.indent
        self.stream += tok[1]
    
    def get_result(self):
        return self.stream.lstrip()
        
RESULT = Formatter()

def element(tok, lex):
    print >>sys.stderr, 'element', tok
    global RESULT
    if tok[0] in [TOK_VAR, TOK_STR]:
        print >>sys.stderr, 'var', tok
        RESULT.add_token(tok, True)
        tok = lex.next()
        if tok[0] == TOK_EQ:
            RESULT.add_token(tok)
            tok = lex.next()
            if tok[0] == TOK_LP:
                RESULT.add_token(tok, True)
                tok = lex.next()
                tok = block(tok, lex)
            elif tok[0] in [TOK_VAR, TOK_STR]:
                RESULT.add_token(tok)
                tok = lex.next()
            else:
                raise
                
    elif tok[0] == TOK_LP:
        RESULT.add_token(tok, True)
        tok = lex.next()
        tok = block(tok, lex)
    return tok
    
def block(tok, lex):
    print >>sys.stderr, 'block', tok
    global RESULT
    RESULT.indent += 1
    tok = element(tok, lex)
    while tok[0] == TOK_SEMI:
        RESULT.add_token(tok)
        tok = lex.next()
        tok = element(tok, lex)
    RESULT.indent -= 1
    if tok[0] == TOK_RP:
        RESULT.add_token(tok, True)
        tok = lex.next()
    return tok
    
    
n = int(raw_input())
text = []
for i in xrange(n):
    text.append(raw_input())
text.append('')  # explicit EOF

lex = get_tokens('\n'.join(text))
try:
    tok = lex.next()
    element(tok, lex)
except StopIteration:
    pass

print RESULT.get_result()
