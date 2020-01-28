from classes.operators.Operator import Operator


class Menor(Operator):
    def __init__(self):

        self.label = 'MENOR'

        super().__init__({
            'identifier': "<"
        })
