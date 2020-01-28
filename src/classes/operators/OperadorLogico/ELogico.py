from classes.operators.Operator import Operator


class ELogico(Operator):
    def __init__(self):

        self.label = 'E_LOGICO'

        super().__init__({
            'identifier': "&&"
        })
