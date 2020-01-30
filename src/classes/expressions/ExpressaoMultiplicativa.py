from classes.Base import Base


class ExpressaoMultiplicativa(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO_MULTIPLICATIVA'

        super().__init__(data)
