from classes.operators.Operator import Operator

class Multiplicacao(Operator):
    def __init__(self):

        self.label = 'MULTIPLICACAO'

        super().__init__({
            'identifier': "*"
        })
