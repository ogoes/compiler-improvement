from classes.operators.Operator import Operator


class Divisao(Operator):
    def __init__(self):

        self.label = 'DIVISAO'

        super().__init__({
            'identifier': "/"
        })
