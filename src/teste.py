

def make(self, a):
    def a():
        return self.__data.get(a)

    return a


class Teste:

    def __init__(self):
        self.__data = {
            "a": 2
        }
        pass

    def a(self):
        return self.a

    def __set__(name):
        def _set(self, value):
            self.__data[name] = value
        return _set

    def __get__(name):
        def _get(self):
            return self.__data.get(name)
        return _get

    def __del__(name):
        def _del(self):
            del self.__data[name]
        return _del

    def __repr__(self):
        return str(self.__data)

    a = property(__get__('a'), __set__('a'), __del__('a'))
    b = property(__get__('b'), __set__('b'), __del__('b'))


# help(int)
teste = Teste()

teste.b = 12
print(teste.__data)
