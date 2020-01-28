from classes.operators.Operator import Operator


class MenorOuIgual(Operator):
    def __init__(self):

        self.label = 'MENOR_IGUAL'

        super().__init__({
            'identifier': "<="
        })
