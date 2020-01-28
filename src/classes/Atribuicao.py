from classes.Base import Base


class Atribuicao(Base):

    def __init__(self, **data):
        data['identifier'] = 'ATRIBUICAO'

        super().__init__(data)
