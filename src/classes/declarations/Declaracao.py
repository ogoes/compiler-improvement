from classes.Base import Base


class Declaracao(Base):

    def __init__(self, **data):
        data['identifier'] = 'DECLARACAO'

        super().__init__(data)
