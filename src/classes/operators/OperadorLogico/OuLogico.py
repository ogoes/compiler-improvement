from classes.operators.Operator import Operator


class Adicao(Operator):
    def __init__(self):

        self.label = 'OU_LOGICO'

        super().__init__({
            'identifier': "||"
        })
