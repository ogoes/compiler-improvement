from classes.Base import Base


class ExpressaoUnaria(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO_UNARIA'

        super().__init__(data)
