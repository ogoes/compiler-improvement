from classes.operators.Operator import Operator

class Subtracao(Operator):
    def __init__(self):
        
        self.label = 'SUBTRACAO'

        super().__init__({
            'identifier': "-"
        })
