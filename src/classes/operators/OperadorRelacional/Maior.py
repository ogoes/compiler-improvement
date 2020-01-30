from classes.operators.Operator import Operator


class Maior(Operator):
    def __init__(self):


        super().__init__({
            'identifier': ">"
        })
        self.label = 'MAIOR'
