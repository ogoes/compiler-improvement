from ply.lex import TOKEN
import ply.lex as lex

import messages.Errors as Errors
import messages

# Aqui estao contidas todas regras lexicas

digito = r"([0-9])"
letra = r"([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ])"
sinal = r"([\-\+]?)"

""" 
    id deve começar com uma letra
"""
id = (
    r"(" + letra + r"(" + digito + r"+|_|" + letra + r")*)"
)  # o mesmo que '((letra)(letra|_|([0-9]))*)'

inteiro = r"(" + sinal + digito + r"+)"


flutuante = (
    r"(" + digito + r"+\." + digito + r"+?)"
)  # o mesmo que (([-\+]?)([0-9]+)\.([0-9]+))'

flutuante = (
    r"(("
    + sinal
    + digito
    + r"+?\."
    + digito
    + r"*?)"
    + r")"
)  # o mesmo que(([0-9]+\.[0-9]*))

notacao_cientifica = (
    r"(" + sinal + r"([1-9])\." + digito + r"+[eE]" + sinal + digito + r"+)"
)  # o mesmo que '(([-\+]?)([1-9])\.([0-9])+[eE]([-\+]?)([0-9]+))'


tokens = [
    "ID",  # identificador
    # numerais
    "NUM_NOTACAO_CIENTIFICA",  # ponto flutuante em notaçao científica
    "NUM_PONTO_FLUTUANTE",  # ponto flutuate
    "NUM_INTEIRO",  # inteiro
    # operadores binarios
    "ADICAO",  # +
    "SUBTRACAO",  # -
    "MULTIPLICACAO",  # *
    "DIVISAO",  # /
    "E_LOGICO",  # &&
    "OU_LOGICO",  # ||
    "DIFERENCA",  # <>
    "MENOR_IGUAL",  # <=
    "MAIOR_IGUAL",  # >=
    "MENOR",  # <
    "MAIOR",  # >
    "IGUALDADE",  # =
    # operadores unarios
    "NEGACAO",  # !
    # simbolos
    "ABRE_PAR",  # (
    "FECHA_PAR",  # )
    "ABRE_COL",  # [
    "FECHA_COL",  # ]
    "VIRGULA",  # ,
    "DOIS_PONTOS",  # :
    "ATRIBUICAO",  # :=
    # 'COMENTARIO', # {***}
]

palavras_reservadas = {
    "se": "SE",
    "então": "ENTAO",
    "senão": "SENAO",
    "fim": "FIM",
    "repita": "REPITA",
    "flutuante": "FLUTUANTE",
    "retorna": "RETORNA",
    "até": "ATE",
    "leia": "LEIA",
    "escreva": "ESCREVA",
    "inteiro": "INTEIRO",
}

tokens = tokens + list(palavras_reservadas.values())


@TOKEN(id)
def t_ID(token):

    token.type = palavras_reservadas.get(
        token.value, "ID"
    )  # não é necessário fazer regras/regex para cada palavra reservada
    # se o token não for uma palavra reservada automaticamente é um id
    # As palavras reservadas têm precedências sobre os ids

    return token


@TOKEN(notacao_cientifica)
def t_NUM_NOTACAO_CIENTIFICA(token):
    return token


@TOKEN(flutuante)
def t_NUM_PONTO_FLUTUANTE(token):
    return token


@TOKEN(inteiro)
def t_NUM_INTEIRO(token):
    return token


def t_ADICAO(token):
    r"\+"
    return token


def t_SUBTRACAO(token):
    r"-"
    return token


def t_MULTIPLICACAO(token):
    r"\*"
    return token


def t_DIVISAO(token):
    r"/"
    return token


def t_E_LOGICO(token):
    r"&&"
    return token


def t_OU_LOGICO(token):
    r"\|\|"
    return token


def t_DIFERENCA(token):
    r"<>"
    return token


def t_MENOR_IGUAL(token):
    r"<="
    return token


def t_MAIOR_IGUAL(token):
    r">="
    return token


def t_MENOR(token):
    r"<"
    return token


def t_MAIOR(token):
    r">"
    return token


def t_IGUALDADE(token):
    r"="
    return token


# operadores unarios
def t_NEGACAO(token):
    r"!"
    return token


# simbolos
def t_ABRE_PAR(token):
    r"\("
    return token


def t_FECHA_PAR(token):
    r"\)"
    return token


def t_ABRE_COL(token):
    r"\["
    return token


def t_FECHA_COL(token):
    r"\]"
    return token


def t_VIRGULA(token):
    r","
    return token


def t_ATRIBUICAO(token):
    r":="
    return token


def t_DOIS_PONTOS(token):
    r":"
    return token


t_ignore = " \t"


# t_COMENTARIO = r'(\{((.|\n)*?)\})'
# para poder contar as quebras de linha dentro dos comentarios
def t_COMENTARIO(token):
    r"(\{((.|\n)*?)\})"
    token.lexer.lineno += token.value.count("\n")
    # return token


def t_newline(token):
    r"\n+"
    token.lexer.lineno += len(token.value)


def define_column(input, lexpos):
    begin_line = input.rfind("\n", 0, lexpos) + 1
    return (lexpos - begin_line) + 1


def t_error(token):

    messages.filename = token.lexer.filename

    Errors.UnknownSymbol(token.value.split()[0], {
        'line': token.lineno,
        'column': define_column(token.lexer.backup_data, token.lexpos)
    })

    token.lexer.skip(1)

    token.lexer.has_error = True


lexer = lex.lex()
