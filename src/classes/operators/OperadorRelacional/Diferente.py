from classes.operators.Operator import Operator


class Diferente(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "<>"
        })
        self.label = 'DIFERENCA'
