#!/usr/bin/python3
from utils import Scope
from pprint import pprint
import re

from lexer.rules import inteiro, flutuante, notacao_cientifica
import ply.yacc as yacc

from classes import *
from classes.Base import Base

from classes.operators import OperadorAditivo, OperadorLogico, OperadorMultiplicativo, OperadorRelacional, Negacao


debug = False


def define_column(input, lexpos):
    begin_line = input.rfind("\n", 0, lexpos) + 1
    return (lexpos - begin_line) + 1


def p_programa(production):
    "programa : lista_declaracoes"

    parser.filedata = parser.filedata or ""

    node = Programa()

    node.insert_node_below(production[1])

    scope = Scope()
    scope.name = 'global'
    scope.begin = {'line': 1, 'column': 1}
    scope.ending = {
        'line': production.linespan(1)[1] + 1,
        'column': define_column(parser.filedata, production.lexspan(1)[1])
    }

    node.scope = scope

    production[0] = node


def p_lista_declaracoes(production):
    """lista_declaracoes : lista_declaracoes declaracao
                        | declaracao
    """

    node = ListaDeDeclaracoes()

    first_node = production[1]

    if first_node.id == "LISTA_DECLARACOES":
        node.insert_node_below(first_node.children)
        node.insert_node_below(production[2])
    else:
        node.insert_node_below(first_node)

    production[0] = node


def p_declaracao(production):
    """declaracao : declaracao_variaveis
                | inicializacao_variaveis
                | declaracao_funcao
    """
    node = Declaracao()
    node.insert_node_below(production[1])
    production[0] = node


def p_declaracao_variaveis(production):
    "declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis"

    node = DeclaracaoDeVariaveis()

    node.insert_node_below(production[1])

    node.insert_node_below(Token(identifier=':'))

    node.insert_node_below(production[3])

    production[0] = node


def p_inicializacao_variaveis(production):
    "inicializacao_variaveis : atribuicao"

    node = InicializacaoDeVariaveis()
    node.insert_node_below(production[1])
    production[0] = node


def p_lista_variaveis(production):
    """lista_variaveis : lista_variaveis VIRGULA var
                    | var
    """

    node = ListaDeVariaveis()

    first_node_name = production[1].id

    if first_node_name == "LISTA_VARIAVEIS":
        node.insert_node_below(production[1].children)

        node.insert_node_below(Token(identifier=','))

        node.insert_node_below(production[3])
    else:
        node.insert_node_below(production[1])

    production[0] = node


def p_var(production):
    """var : ID
        | ID indice
    """

    node = Variavel()

    id_node = Id(identifier=production[1])
    node.insert_node_below(id_node)

    production_length = len(production)
    if production_length == 3:
        node.insert_node_below(production[2])

    production[0] = node


def p_indice(production):
    """indice : indice ABRE_COL expressao FECHA_COL
            | ABRE_COL expressao FECHA_COL
    """

    node = Indice()

    production_length = len(production)

    col_index = 1

    if production_length == 5:
        node.insert_node_below(production[col_index].children)
        col_index += 1

    node.insert_node_below(Token(identifier='['))

    node.insert_node_below(production[col_index + 1])

    node.insert_node_below(Token(identifier=']'))
    production[0] = node


def p_indice_error(production):
    """indice : ABRE_COL  error
            | error  FECHA_COL
            | ABRE_COL error FECHA_COL
            | indice ABRE_COL  error
            | indice error  FECHA_COL
            | indice ABRE_COL error FECHA_COL

    """

    index = 0

    message = ""
    typeof = "MISSING_SYMBOL"
    token = None

    if len(production) == 4 and production[1] != "[":
        index += 1

    if production[index + 1] == "[":
        index += 2
        message = "']' é esperado"

    elif production[index + 2] == "]":
        index += 1
        message = "'[' é esperado"

    if production[1] == "[":
        typeof = " BLANK_CONTENT"
        message = "expressão vazia"
        index = 2

    if len(production) == 5:
        index = 3
        typeof = " BLANK_CONTENT"
        message = "expressão vazia"
        pass

    token = production[index]
    token.column = define_column(token.lexer.backup_data, token.lexpos)

    error = {
        "file": False,
        "type": typeof,
        "message": message,
        "value": token.value,
        "position": (token.lineno, token.column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    parser.errok()

    pass


def p_tipo(production):
    """tipo : INTEIRO
        | FLUTUANTE
    """

    node = Tipo()

    value = "inteiro" if production[1] == "inteiro" else "flutuante"

    node.rtype = value

    production[0] = node


def p_declaracao_funcao(production):
    """declaracao_funcao : tipo cabecalho 
                        | cabecalho 
    """

    node = DeclaracaoDeFuncao()

    production_length = len(production)

    index = 1

    if production_length == 2:
        tipo = Tipo()
        tipo.rtype = 'vazio'
        node.insert_node_below(tipo)
    else:
        node.insert_node_below(production[index])
        index += 1

    node.insert_node_below(production[index])

    production[0] = node


def p_cabecalho_error(production):
    """cabecalho : ID error lista_parametros FECHA_PAR corpo FIM
                | ID ABRE_PAR lista_parametros error corpo FIM
                | ID ABRE_PAR lista_parametros FECHA_PAR corpo 
    """

    value = None

    message = ""

    index = 0

    if production[2] == "(" and production[4] == ")":
        index = 5
        value = "fim"
        message = "token 'fim' não encontrado"

    elif production[2] == "(":

        index = 4
        # token = production[4]
        message = "')' é esperado"

    elif production[4] == ")":
        index = 2
        # token = production[2]
        message = "'(' é esperado"
        # print("O símbolo ')' é esperado em um cabeçalho de um função")

    line = production.linespan(index)[1]
    pos = production.lexspan(index)[1]

    column = define_column(parser.filedata, pos)
    error = {
        "file": True,
        "type": "MISSING_SYMBOL",
        "message": message,
        "value": value,
        "position": (line, column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    parser.errok()


def p_cabecalho(production):
    "cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM"

    node = Cabecalho()

    node.insert_node_below(Id(identifier=production[1]))

    scope = Scope()

    scope.id = production[1]
    scope.begin = {
        "line": production.linespan(1)[1],
        "column": define_column(parser.filedata, production.lexspan(1)[1])
    }
    scope.ending = {
        "line": production.linespan(6)[0],
        "column": define_column(parser.filedata, production.lexspan(6)[0])
    }

    node.insert_node_below(Token(identifier='('))
    node.insert_node_below(production[3])
    node.insert_node_below(Token(identifier=')'))
    node.insert_node_below(production[5])
    node.insert_node_below(Token(identifier='fim'))

    node.scope = scope

    production[0] = node


def p_lista_parametros(production):
    """lista_parametros : lista_parametros VIRGULA parametro
                    | parametro
                    | vazio
    """

    node = ListaDeParametros()

    first_node_name = production[1].id
    if first_node_name == "LISTA_PARAMETROS":
        node.insert_node_below(production[1].children)
        node.insert_node_below(production[3])

    else:
        node.insert_node_below(production[1])

    production[0] = node


def p_parametro(production):
    """parametro : tipo DOIS_PONTOS ID
                | parametro ABRE_COL FECHA_COL
    """

    node = Parametro()
    first_name = production[1].id

    if first_name == "TIPO":
        node.insert_node_below(production[1])
        node.insert_node_below(Token(identifier=':'))
        node.insert_node_below(Id(identifier=production[3]))

    else:
        parametro = production[1]
        parametro.insert_node_below(Token(identifier='['))
        parametro.insert_node_below(Token(identifier=']'))
        node = parametro

    production[0] = node


def p_parametro_error(production):
    """parametro : tipo error ID
                | error ID
                | parametro error FECHA_COL
                | parametro ABRE_COL error
    """

    index = 2

    if production[index] == "[":
        index += 1

    token = production[index]

    value = None
    line = None
    column = define_column(parser.filedata, production.lexspan(index)[0])
    message = ""

    if index == 2:
        message = "Tipo do Parâmetro não especificado"
        value = token
        line = production.linespan(index)
        # help(production[1])
    else:
        value = token.value
        line = token.lineno
        if token.type == "ID":
            message = "':' é esperado na definição de parâmetros"
        elif token.type == "FECHA_COL":
            message = "'[' é esperado"
        elif token.type != "FECHA_COL":
            message = "']' é esperado"

    error = {
        "file": False,
        "type": "MISSING_SYMBOL",
        "message": message,
        "value": value,
        "position": (line, column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    # parser.errok()
    pass


def p_corpo(production):
    """corpo : corpo acao
            | vazio
    """

    node = Corpo()

    first_name = production[1].id

    if first_name == "CORPO":
        node.insert_node_below(production[1].children)
        node.insert_node_below(production[2])
    else:
        node.insert_node_below(production[1])

    production[0] = node


def p_acao(production):
    """acao : expressao
        | declaracao_variaveis
        | se
        | repita
        | leia
        | escreva
        | retorna
    """

    node = Acao()

    node.insert_node_below(production[1])

    production[0] = node


def p_se_error(production):
    """se : error expressao ENTAO corpo FIM
        | SE expressao error corpo FIM
        | error expressao ENTAO corpo SENAO corpo FIM
        | SE expressao error corpo SENAO corpo FIM
        | SE expressao ENTAO corpo error corpo FIM
        | SE expressao ENTAO corpo SENAO corpo
    """

    message = ""
    index = 1
    if production[index] == "se":
        index += 2
    if production[index] == "então":
        index += 2
    if production[index] == "senão":
        index += 1

    line = production.linespan(index)[1]
    pos = production.lexspan(index)[1]

    value = production[index]
    column = define_column(parser.filedata, pos)

    if index == 1:
        message = "erro com o identificador de estrutura condicional 'se'"

    elif index == 3:
        message = "o token 'então' não foi identificado"

    elif index == 5:
        message = "o token 'senão' não foi identificado"

    elif index == 7:
        message = "o token 'fim' não foi identificado"

    error = {
        "file": False,
        "type": "MISSING_TOKEN",
        "message": message,
        "value": value,
        "position": (line, column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    parser.errok()
    pass


def p_se(production):
    """se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM
    """

    node = Se()

    scope = Scope()

    scope.name = "se.então"
    scope.begin = {
        'line': production.linespan(3)[1],
        'column': define_column(parser.filedata, production.lexspan(3)[1])
    }
    scope.ending = {
        'line': production.linespan(5)[0],
        'column': define_column(parser.filedata, production.lexspan(5)[0])
    }

    production[4].scope = scope

    node.insert_node_below(Token(identifier='se'))
    node.insert_node_below(production[2])
    node.insert_node_below(Token(identifier='então'))
    node.insert_node_below(production[4])

    if len(production) == 8:
        node.insert_node_below(Token(identifier='senão'))

        senao_scope = Scope()

        senao_scope.name = "se.senão"
        senao_scope.begin = {
            'line': production.linespan(5)[1],
            'column': define_column(parser.filedata, production.lexspan(5)[1])
        }
        senao_scope.ending = {
            'line': production.linespan(7)[0],
            'column': define_column(parser.filedata, production.lexspan(7)[0])
        }

        production[6].scope = senao_scope
        node.insert_node_below(production[6])

    node.insert_node_below(Token(identifier='fim'))
    production[0] = node


def p_repita(production):
    "repita : REPITA corpo ATE expressao"

    node = Repita()

    scope = Scope()

    scope.name = 'repita'
    scope.begin = {
        'line': production.linespan(1)[1],
        'column': define_column(parser.filedata, production.lexspan(1)[1])
    }
    scope.ending = {
        'line': production.linespan(3)[0],
        'column': define_column(parser.filedata, production.lexspan(3)[0])
    }

    production[2].scope = scope

    node.insert_node_below(Token(identifier='repita'))
    node.insert_node_below(production[2])
    node.insert_node_below(Token(identifier='até'))
    node.insert_node_below(production[4])

    production[0] = node


def p_repita_error(production):
    """repita : error corpo ATE expressao
            | REPITA corpo error expressao
    """

    message = ""
    index = 1

    if production[1] == "repita":
        index += 2
        message = "token 'até' não foi reconhecido"
    else:
        message = "token 'repita' não foi reconhecido"
        pass

    token = production[index]
    token.column = define_column(token.lexer.backup_data, token.lexpos)

    error = {
        "file": False,
        "type": "MISSING_TOKEN",
        "message": message,
        "value": token.value,
        "position": (token.lineno, token.column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    parser.errok()
    pass


def p_atribuicao(production):
    "atribuicao : var ATRIBUICAO expressao"

    node = Atribuicao()

    node.insert_node_below(production[1])
    node.insert_node_below(Token(identifier=':='))
    node.insert_node_below(production[3])

    production[0] = node


def p_leia(production):
    "leia : LEIA ABRE_PAR var FECHA_PAR"

    node = Leia()

    node.insert_node_below(Token(identifier='leia'))
    node.insert_node_below(Token(identifier='('))
    node.insert_node_below(production[3])
    node.insert_node_below(Token(identifier=')'))

    production[0] = node


def p_leia_error(production):
    """leia : LEIA ABRE_PAR error FECHA_PAR
    """

    token = production[3]

    token.column = define_column(parser.filedata, token.lexpos)

    error = {
        "file": False,
        "type": "INVALID_PARAMETER",
        "message": "o parâmetro da função 'leia' deve ser uma variavel",
        "value": token,
        "position": (token.lineno, token.column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    parser.errok()
    pass


def p_escreva(production):
    "escreva : ESCREVA ABRE_PAR expressao FECHA_PAR"

    node = Escreva()

    node.insert_node_below(Token(identifier='escreva'))
    node.insert_node_below(Token(identifier='('))
    node.insert_node_below(production[3])
    node.insert_node_below(Token(identifier=')'))

    production[0] = node


def p_retorna(production):
    "retorna : RETORNA ABRE_PAR expressao FECHA_PAR"

    node = Retorna()

    node.insert_node_below(Token(identifier='retorna'))
    node.insert_node_below(Token(identifier='('))
    node.insert_node_below(production[3])
    node.insert_node_below(Token(identifier=')'))

    production[0] = node


def p_expressao(production):
    """expressao : expressao_logica
                | atribuicao
    """

    node = Expressao()
    node.insert_node_below(production[1])
    production[0] = node


def p_expressao_logica(production):
    """expressao_logica : expressao_simples
                    | expressao_logica operador_logico expressao_simples
    """

    node = ExpressaoLogica()

    second_name = production[1].id
    node.insert_node_below(production[1])

    if second_name == "EXPRESSAO_LOGICA":
        node.insert_node_below(production[2])
        node.insert_node_below(production[3])

    production[0] = node


def p_expressao_simples(production):
    """expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva
    """

    node = ExpressaoSimples()

    second_name = production[1].id
    node.insert_node_below(production[1])

    if second_name == "EXPRESSAO_SIMPLES":
        node.insert_node_below(production[2])
        node.insert_node_below(production[3])

    production[0] = node


def p_expressao_aditiva(production):
    """expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa
    """

    node = ExpressaoAditiva()

    second_name = production[1].id
    node.insert_node_below(production[1])

    if second_name == "EXPRESSAO_ADITIVA":
        node.insert_node_below(production[2])
        node.insert_node_below(production[3])

    production[0] = node


def p_expressao_multiplicativa(production):
    """expressao_multiplicativa : expressao_unaria
                                                        | expressao_multiplicativa operador_multiplicacao expressao_unaria
        """

    node = ExpressaoMultiplicativa()

    second_name = production[1].id
    node.insert_node_below(production[1])

    if second_name == "EXPRESSAO_MULTIPLICATIVA":
        node.insert_node_below(production[2])
        node.insert_node_below(production[3])

    production[0] = node


def p_expressao_unaria(production):
    """expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
        """

    node = ExpressaoUnaria()

    node.insert_node_below(production[1])

    second_name = production[1].id

    if second_name != "FATOR":
        node.insert_node_below(production[2])

    production[0] = node


def p_operador_relacional(production):
    """operador_relacional : MENOR
                            | MAIOR
                            | IGUALDADE
                            | DIFERENCA 
                            | MENOR_IGUAL
                            | MAIOR_IGUAL
    """

    Obj = None

    if production[1] == "<":
        Obj = OperadorRelacional.Menor
    elif production[1] == ">":
        Obj = OperadorRelacional.Maior
    elif production[1] == "=":
        Obj = OperadorRelacional.Igual
    elif production[1] == "<>":
        Obj = OperadorRelacional.Diferente
    elif production[1] == "<=":
        Obj = OperadorRelacional.MenorOuIgual
    elif production[1] == ">=":
        Obj = OperadorRelacional.MaiorOuIgual

    production[0] = Obj()


def p_operador_soma(production):
    """operador_soma : ADICAO
                    | SUBTRACAO
    """

    Obj = OperadorAditivo.Adicao if production[1] == "+" else OperadorAditivo.Subtracao

    production[0] = Obj()


def p_operador_logico(production):
    """operador_logico : E_LOGICO
                    | OU_LOGICO
    """

    Obj = OperadorLogico.ELogico if production[1] == "&&" else OperadorLogico.OuLogico

    production[0] = Obj()


def p_operador_negacao(production):
    "operador_negacao : NEGACAO"

    production[0] = Negacao()


def p_operador_multiplicacao(production):
    """operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO
        """

    Obj = OperadorMultiplicativo.Multiplicacao if production[
        1] == '*' else OperadorMultiplicativo.Divisao

    production[0] = Obj()


def p_fator(production):
    """fator : ABRE_PAR expressao FECHA_PAR
            | var
            | chamada_funcao
            | numero
        """

    node = Fator()

    production_length = len(production)

    if production_length == 4:
        node.insert_node_below(Token(identifier=production[1]))
        node.insert_node_below(production[2])
        node.insert_node_below(Token(identifier=production[3]))
    else:
        node.insert_node_below(production[1])

    production[0] = node


def p_fator_error(production):
    """fator : ABRE_PAR expressao 
    """

    line = 0
    column = 0
    value = None
    message = ""

    if production[1] == "(":

        message = "')' é esperado"
        value = ")"

        line = production.linespan(2)[1]
        column = define_column(parser.filedata, production.lexspan(2)[1])
    else:
        message = "'(' é esperado"
        value = "("

        line = production.linespan(1)[0]
        column = define_column(parser.filedata, production.lexspan(1)[0])

    error = {
        "file": True,
        "type": "MISSING_SYMBOL",
        "message": message,
        "value": value,
        "position": (line, column),
    }

    try:
        if parser.error_list:
            pass
    except AttributeError:
        parser.error_list = []

    parser.error_list += [error]

    production.error()
    pass


def p_numero(production):
    """numero : NUM_INTEIRO
            | NUM_PONTO_FLUTUANTE
            | NUM_NOTACAO_CIENTIFICA
        """

    rtype = ''

    if re.match(inteiro, production[1]):
        rtype = 'inteiro'
    elif re.match(notacao_cientifica, production[1]):
        rtype = 'flutuante'
    if re.match(flutuante, production[1]):
        rtype = 'flutuante'

    node = Numero()
    node.value = production[1]
    node.rtype = rtype

    production[0] = node


def p_chamada_funcao(production):
    "chamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PAR"

    node = ChamadaDeFuncao()

    node.insert_node_below(Id(identifier=production[1]))
    node.insert_node_below(Token(identifier=production[2]))
    node.insert_node_below(production[3])
    node.insert_node_below(Token(identifier=production[3]))

    production[0] = node


def p_lista_argumentos(production):
    """lista_argumentos : lista_argumentos VIRGULA expressao
                    | expressao
                    | vazio
        """

    node = ListaDeArgumentos()

    first_name = production[1].id

    if first_name == "LISTA_ARGUMENTOS":
        node.insert_node_below(production[1].children)
        node.insert_node_below(Token(identifier=','))
        node.insert_node_below(production[3])
    else:
        node.insert_node_below(production[1])

    production[0] = node


def p_vazio(production):
    "vazio : "

    production[0] = Vazio()


def p_error(production):

    if production:
        token = production
        parser.filename = token.lexer.filename
        token.column = define_column(token.lexer.backup_data, token.lexpos)
        error = {
            "file": True,
            "type": "  SYNTAX_ERROR",
            "message": "erro próximo ao token '{token}'".format(token=token.value),
            "value": token.value,
            "position": (token.lineno, token.column),
        }

        try:
            if parser.error_list:
                pass
        except AttributeError:
            parser.error_list = []

        parser.error_list += [error]
    pass


parser = yacc.yacc(start="programa")
