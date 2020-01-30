from classes.Base import Base


class ExpressaoAditiva(Base):

    def __init__(self, **data):
        data['identifier'] = 'EXPRESSAO_ADITIVA'

        super().__init__(data)
