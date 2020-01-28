from classes.Base import Base


class Repita(Base):

    def __init__(self, **data):
        data['identifier'] = 'REPITA'
        
        super().__init__(data)
