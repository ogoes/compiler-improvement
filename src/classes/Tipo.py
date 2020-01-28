from classes.Base import Base


class Tipo(Base):

    def __init__(self, **data):
        data['identifier'] = 'TIPO'
        
        super().__init__(data)
