from classes.Base import Base


class InicializacaoDeVariaveis(Base):

    def __init__(self, **data):
        data['identifier'] = 'INICIALIZACAO_VARIAVEIS'

        super().__init__(data)
