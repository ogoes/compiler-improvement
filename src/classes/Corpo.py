from classes.Base import Base


class Corpo(Base):

    def __init__(self, **data):
        data['identifier'] = 'CORPO'
        
        super().__init__(data)
