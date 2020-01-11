

class Base:
    """
    """

    def __init__(self, data: dict = None):
        """
            Constructor --
                data = {
                    "type": [PROGRAMA, ID, SE]
                    "scope": [Node's scope]
                    "operation": [What this Node do?]
                    "visible_scopes": [What attributes this Node can access?]
                    "callable": [It's a function?]
                    "variable": [It's a variable?]
                    "dimentions": [If is a vector, yours dimentions]
                    "return_type": [Node return type ('inteiro'|'flutuante'|'vazio')]
                    "identifier": [Name|Number found in code]
                    "children": [Adjacent Nodes in tree]
                    "params_types": [If is a function, yours parameters attributes]
                }

        """

        if not data.get('type'):
            raise "Tipo não especificado"
        if not data.get('type'):
            raise "Operação não especificada"
        if not data.get('type'):
            raise "Identificador não especificado"

        self.__data = data
        self.visible_scopes = data.get('visible_scopes') or []
        self.dimentions = data.get('dimentions') or []
        self.children = data.get('children') or []
        self.params_types = data.get('params_types') or []
        self.rtype = data.get('return_type') or 'vazio'


        self.__reduced = False

    def __repr__(self):
        representation = f"{self.type}:{self.identifier}"
        if self.callable:
            representation += "  --> FUNCTION"
        elif self.variable:
            representation += "  --> VARIABLE"

        if self.scope:
            representation += f"\n\tSCOPE: {str(self.scope)}"
        if self.operation:
            representation += f"\n\tOPERATION: {self.operation}"
        if self.visible_scopes:
            representation += f"\n\tVISIBLE_SCOPES: {str(self.type)}"
        if self.dimentions:
            representation += f"\n\tDIMENTIONS: {str([item.get('size') for item in self.dimentions])}"
        if self.return_type:
            representation += f"\n\tRETURN_TYPE: {self.return_type}"

        representation += f"\n\tCHILDREN: {[str(item) for item in self.children]}"

        if self.params_types:
            representation += f"\n\PARAMS: {str([item.get('type') for item in self.params_types])}"

    def __str__(self):
        return f"{self.type}:{self.identifier}"

    def __set__(name):
        def _set(self, value):
            if name == 'scope':
                if not self.scope:
                    self.__data[name] = value

                for adj in self.children:
                    adj.scope = value

                self.visible_scopes = self.visible_scopes + [value]

            else:
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

    def insert_node_below(self, node):
        if type(node) is list:
            for node_adj in node:
                node_adj.set_scope(self.__scope)
                self.insert_node_below(node_adj)
        else:
            self.__above.append(node)
        pass

    def is_variable(self):
        return self.variable or False

    def is_function(self):
        return self.callable or False

    def reduce(self):
        pass
    def semantic_a(self):
        pass
    def generator(self, builder):
        pass

    type = property(__get__('type'), __set__('type'), __del__('type'))
    
    scope = property(__get__('scope'), __set__('scope'), __del__('scope'))
    
    operation = property(__get__('operation'), __set__(
        'operation'), __del__('operation'))
    
    visible_scopes = property(__get__('visible_scopes'), __set__(
        'visible_scopes'), __del__('visible_scopes'))
    
    dimentions = property(__get__('dimentions'), __set__(
        'dimentions'), __del__('dimentions'))
    
    rtype = property(__get__('return_type'), __set__(
        'return_type'), __del__('return_type'))
    
    id = property(__get__('identifier'), __set__(
        'identifier'), __del__('identifier'))
    
    children = property(__get__('children'), __set__(
        'children'), __del__('children'))
    
    params_types = property(__get__('params_types'), __set__(
        'params_types'), __del__('params_types'))
