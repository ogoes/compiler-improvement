from classes.Base import Base


class Programa(Base):

    def __init__(self, **data):
        data['identifier'] = "PROGRAMA"

        super().__init__(data)
