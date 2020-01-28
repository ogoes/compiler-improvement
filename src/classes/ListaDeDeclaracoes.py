from classes.Base import Base


class ListaDeDeclaracoes(Base):

    def __init__(self, **data):
        data['identifier'] = 'LISTA_DECLARACOES'


        super().__init__(data)
