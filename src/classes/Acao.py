from classes.Base import Base


class Acao(Base):

    def __init__(self, **data):
        data['identifier'] = 'ACAO'
        
        super().__init__(data)
