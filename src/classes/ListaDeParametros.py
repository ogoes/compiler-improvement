from classes.Base import Base


class ListaDeParametros(Base):

    def __init__(self, **data):
        data['identifier'] = 'LISTA_PARAMETROS'
        super().__init__(data)
