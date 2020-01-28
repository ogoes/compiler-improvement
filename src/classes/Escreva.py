from classes.Base import Base


class Escreva(Base):

    def __init__(self, **data):
        data['identifier'] = 'ESCREVA'

        super().__init__(data)
