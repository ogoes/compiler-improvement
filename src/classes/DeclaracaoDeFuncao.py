from classes.Base import Base


class DeclaracaoDeFuncao(Base):

    def __init__(self, **data):
        data['identifier'] = 'DECLARACAO_FUNCAO'
        
        super().__init__(data)
