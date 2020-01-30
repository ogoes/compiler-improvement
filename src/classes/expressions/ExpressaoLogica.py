from classes.Base import Base


class ExpressaoLogica(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO_LOGICA'

        super().__init__(data)
