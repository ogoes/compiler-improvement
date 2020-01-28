from classes.operators.Operator import Operator


class Igual(Operator):
    def __init__(self):

        self.label = 'IGUALDADE'

        super().__init__({
            'identifier': "="
        })
