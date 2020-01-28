from classes.operators.Operator import Operator


class Maior(Operator):
    def __init__(self):

        self.label = 'MAIOR'

        super().__init__({
            'identifier': ">"
        })
