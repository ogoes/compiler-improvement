from classes.operators.Operator import Operator


class Divisao(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "/"
        })
        self.label = 'DIVISAO'
