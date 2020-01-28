from classes.operators.Operator import Operator


class Negacao(Operator):
    def __init__(self):

        self.label = 'NEGACAO'

        super().__init__({
            'identifier': "!"
        })
