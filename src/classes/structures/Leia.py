from classes.Base import Base


class Leia(Base):

    def __init__(self, **data):
        data['identifier'] = 'LEIA'

        super().__init__(data)
