from classes.Base import Base


class ListaDeArgumentos(Base):

    def __init__(self, **data):
        data['identifier'] = 'LISTA_ARGUMENTOS'

        super().__init__(data)
