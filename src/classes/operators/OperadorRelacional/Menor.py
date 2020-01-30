from classes.operators.Operator import Operator


class Menor(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "<"
        })
        self.label = 'MENOR'
