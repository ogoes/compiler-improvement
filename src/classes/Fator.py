from classes.Base import Base


class Fator(Base):

    def __init__(self, **data):
        data['identifier'] = 'FATOR'
        
        super().__init__(data)
