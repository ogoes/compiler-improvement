from classes.Base import Base


class Indice(Base):

    def __init__(self, **data):
        data['identifier'] = 'INDICE'
        
        super().__init__(data)
