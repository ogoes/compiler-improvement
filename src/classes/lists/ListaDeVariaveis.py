from classes.Base import Base


class ListaDeVariaveis(Base):

    def __init__(self, **data):
        data['identifier'] = 'LISTA_VARIAVEIS'
        
        super().__init__(data)
