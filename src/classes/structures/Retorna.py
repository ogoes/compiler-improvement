from classes.Base import Base


class Retorna(Base):

    def __init__(self, **data):
        data['identifier'] = 'RETORNA'

        super().__init__(data)
