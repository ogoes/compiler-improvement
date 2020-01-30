from classes.operators.Operator import Operator


class ELogico(Operator):
    def __init__(self):


        super().__init__({
            'identifier': "&&"
        })
        self.label = 'E_LOGICO'
