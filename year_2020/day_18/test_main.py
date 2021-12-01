from sly import Lexer, Parser


class Lexer(Lexer):
    tokens = { NUMBER, PLUS, TIMES, LPAREN, RPAREN }
    ignore = ' \t'

    NUMBER = r'\d+'
    PLUS = r'\+'
    TIMES = r'\*'
    LPAREN = r'\('
    RPAREN = r'\)'


class Parser(Parser):
    tokens = Lexer.tokens

    precedence = (
        ('left', PLUS, TIMES),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)


class Parser2(Parser):
    tokens = Lexer.tokens

    precedence = (
        ('left', TIMES),
        ('left', PLUS),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)



lexer = Lexer()
parser = Parser()
parser2 = Parser2()


def evaluate(expr):
    return parser.parse(lexer.tokenize(expr))


def evaluate2(expr):
    return parser2.parse(lexer.tokenize(expr))


def test_evaluate():
    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert evaluate('2 * 3 + (4 * 5)') == 26
    assert evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632


def test_evaluate2():
    assert evaluate2('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert evaluate2('2 * 3 + (4 * 5)') == 46
    assert evaluate2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
    assert evaluate2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
    assert evaluate2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340


if __name__ == '__main__':
    input_ = open('input.txt').read().rstrip('\n').split('\n')
    s = sum(evaluate(e) for e in input_)
    print('part1:', s)
    s = sum(evaluate2(e) for e in input_)
    print('part2:', s)
