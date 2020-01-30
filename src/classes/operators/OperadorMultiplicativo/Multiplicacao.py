from classes.operators.Operator import Operator

class Multiplicacao(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "*"
        })
        self.label = 'MULTIPLICACAO'
