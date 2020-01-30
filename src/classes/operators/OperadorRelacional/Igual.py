from classes.operators.Operator import Operator


class Igual(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "="
        })
        self.label = 'IGUALDADE'
