from classes.operators.Operator import Operator

class Subtracao(Operator):
    def __init__(self):
        

        super().__init__({
            'identifier': "-"
        })
        self.label = 'SUBTRACAO'
