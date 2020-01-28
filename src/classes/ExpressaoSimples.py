from classes.Base import Base


class ExpressaoSimples(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO_SIMPLES'

        super().__init__(data)
