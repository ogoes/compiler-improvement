from classes.Base import Base


class Token(Base):
    def __init__(self, **data):

        self.label = 'TOKEN'

        super().__init__(data)
