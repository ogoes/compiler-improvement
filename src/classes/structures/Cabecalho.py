from classes.Base import Base


class Cabecalho(Base):

    def __init__(self, **data):
        data['identifier'] = 'CABECALHO'
        
        super().__init__(data)
