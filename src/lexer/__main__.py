
import sys


sys.path.append(sys.path[0] + '/../')

import re
import argparse
from pprint import pprint


from ply.lex import lex
from lexer import define_column

import lexer as lexer_rules


parser = argparse.ArgumentParser()


def tokenizer(data, filename=None):
    lexer = lex(module=lexer_rules)

    lexer.input(data)
    lexer.backup_data = data
    lexer.cerro = []

    file = r"[a-zA-Z0-9_-]+\.tpp"
    lexer.filename = re.findall(file, filename)[0]

    tokens = []

    for token in lexer:
        token.col = define_column(data, token.lexpos)
        tokens.append(
            {
                "token": token.type,
                "value": token.value,
                "lineno": token.lineno,
                "colno": token.col,
                "position": token.lexpos,
            }
        )
        pass

    return {
        "erro": None if len(lexer.cerro) == 0 else lexer.cerro,
        "token": tokens,  # tokens, value, lineno, colno, position
    }

def show_data(data):
    data = results.get("token")
    for item in data:
        if not args.color:
            pass
        else:
            print("<%s, '%s'>" % (item["token"], item["value"]))
    pass


if __name__ == "__main__":

    parser.add_argument("-f", "--file", help="Filename",
                        required=True, type=str)
    parser.add_argument(
        "-c", "--color", help="Disable Colors", action="store_true")
    args = parser.parse_args()
    ## tratamento de argumentos

    if not re.search(r"\.tpp$", args.file):  # testa a extensão do arquivo
        filename = re.findall(r"[a-zA-Z0-9_-]+\.[a-z]*", args.file)[0]
        print(filename, end=": ")
        if not args.color:
            pass
        else:
            print("ERRO: Formato de arquivo não esperado")

        exit(2)

    with open(args.file, "r") as file:  # operacoes com o arquivo
        filedata = file.read()
        file.close()

    results = tokenizer(filedata, args.file)

    ## mostra dados caso não haja erros
    # pprint(results)
    show_data(results)
