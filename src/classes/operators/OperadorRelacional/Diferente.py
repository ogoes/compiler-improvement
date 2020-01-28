from classes.operators.Operator import Operator


class Diferente(Operator):
    def __init__(self):

        self.label = 'DIFERENCA'

        super().__init__({
            'identifier': "<>"
        })
