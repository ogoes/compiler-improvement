from classes.operators.Operator import Operator


class MaiorOuIgual(Operator):
    def __init__(self):

        self.label = 'MAIOR_IGUAL'

        super().__init__({
            'identifier': ">="
        })
