from classes.Base import Base


class DeclaracaoDeVariaveis(Base):

    def __init__(self, **data):
        data['identifier'] = 'DECLARACAO_VARIAVEIS'

        super().__init__(data)
