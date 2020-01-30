from classes.Base import Base


class Expressao(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO'

        super().__init__(data)
