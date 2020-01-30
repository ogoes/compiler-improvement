from classes.operators.Operator import Operator


class Adicao(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "+"
        })
        self.label = 'ADICAO'
