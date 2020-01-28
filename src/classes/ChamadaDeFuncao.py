from classes.Base import Base


class ChamadaDeFuncao(Base):

    def __init__(self, **data):
        data['identifier'] = 'CHAMADA_FUNCAO'
        
        super().__init__(data)
