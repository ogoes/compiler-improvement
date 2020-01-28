

from classes.Base import Base


class Operator(Base):
    def __init__(self, data):
        self.label = 'OPERATOR'
        super().__init__(data)
