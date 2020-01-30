from classes.Base import Base


class Se(Base):

    def __init__(self, **data):
        data['identifier'] = 'SE'
        
        super().__init__(data)


