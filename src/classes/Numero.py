from classes.Base import Base


class Numero(Base):

    def __init__(self, **data):
        data['identifier'] = 'NUMERO'
        
        super().__init__(data)
