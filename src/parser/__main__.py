#!/usr/bin/python3

import sys
sys.path.append(sys.path[0] + '/../')



from pprint import pprint
from lexer import lexer, tokens

from productions import parser

import ply.yacc as yacc
import re
import argparse
from graphviz import Graph



parse = argparse.ArgumentParser()
parse.add_argument("-f", "--file", help="Filename", required=True, type=str)

args = parse.parse_args()


def get_file_data():
    with open(args.file, "r") as file:  # operacoes com o arquivo
        filedata = file.read()
        file.close()

    return filedata


def create_ete_image(tree, source_filename, reduced):
    from ete3 import TreeStyle

    last = source_filename.rfind(".")
    result_filename = source_filename[:last]

    ts = TreeStyle()

    ts.branch_vertical_margin = 20
    ts.scale_length = 15
    ts.tree_width = 10
    ts.scale = 2

    rd = "_reduced" if reduced else ""

    tree.render(result_filename + rd + ".png", w=5000, tree_style=ts)
    # print(tree)

    pass


if __name__ == "__main__":

    filedata = get_file_data()

    lexer.backup_data = filedata

    lexer.filename = re.findall(r"[a-zA-Z0-9_-]+\.tpp", args.file)[0]
    lexer.has_error = False


    parser.filedata = filedata
    parser.filename = lexer.filename


    tree_root = parser.parse(filedata, lexer=lexer, tracking=True)

    tree = None
    if tree_root:

        tree = tree_root.graphic_repr()

        if tree:
           tree.render('output.gv')

    else:
        exit(1)

    # graph.render()
