from classes.operators.Operator import Operator


class Adicao(Operator):
    def __init__(self):

        self.label = 'ADICAO'

        super().__init__({
            'identifier': "+"
        })
