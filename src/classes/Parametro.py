from classes.Base import Base


class Parametro(Base):

    def __init__(self, **data):
        data['identifier'] = 'PARAMETRO'
        super().__init__(data)
