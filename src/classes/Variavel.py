from classes.Base import Base


class Variavel(Base):

    def __init__(self, **data):
        data['identifier'] = 'VAR'
        
        super().__init__(data)
