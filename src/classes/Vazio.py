from classes.Base import Base


class Vazio(Base):
    def __init__(self, **data):
        data['identifier'] = 'VAZIO'
        
        super().__init__(data)
