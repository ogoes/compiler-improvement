from classes.operators.Operator import Operator


class OuLogico(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "||"
        })
        self.label = 'OU_LOGICO'
