

class Scope:

    __scope_id = 0

    def __init__(self, data=None):

        self.__data = data or {}
        self.__data['id'] = Scope.__scope_id

        Scope.__scope_id += 1


    def __get__(attr): return lambda self: self.__data.get(attr)

    def __set__(attr):
        def _set(self, value):
            if self.__data.get(attr) != None:
                raise Exception(
                    f'Não é possível redifinir o valor de \'{attr}\'')

            if attr == 'begin' or attr == 'ending':
                if not isinstance(value, dict):
                    raise Exception(
                        'O valor deve ser do tipo dict e conter os atributos \'line\' e \'column\'.')
                elif value.get('line') == None or not isinstance(value.get('line'), int):
                    raise Exception('Deve haver o atributo inteiro \'line\'')
                elif value.get('column') == None or not isinstance(value.get('column'), int):
                    raise Exception('Deve haver o atributo inteiro \'column\'')
                else:
                    data = {}
                    data['line'] = value.get('line')
                    data['column'] = value.get('column')
                    value = data

            self.__data[attr] = value

        return _set

    def __repr__(self):
        return f'{self.id}:{self.name}:[{self.begin.get("line")}-{self.begin.get("column")}]:[{self.ending.get("line")}-{self.ending.get("column")}]'

    def __mul__(self, value):
        ret = [self]
        for _ in range(value - 1):
            ret.append(Scope())
        return ret

    name = property(__get__('name'), __set__('name'))
    id = property(__get__('id'), __set__('id'))
    begin = property(__get__('begin'), __set__('begin'))
    ending = property(__get__('ending'), __set__('ending'))


scope = Scope()
scope.begin = {'line': 1, 'column': 2}
scope.ending = {'line': 1, 'column': 2}

scopes = [scope] + Scope() * 4


if scope in scopes[::-1]:
    print(scope)
