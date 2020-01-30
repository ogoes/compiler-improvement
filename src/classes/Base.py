
from graphviz import Graph
class Base:
    """
    """

    __id = 0
    __digraph = Graph()

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
        




        if not data.get('identifier'):
            raise Exception("Identificador não especificado")

        self.__data = data
        self.visible_scopes = data.get('visible_scopes') or []
        self.dimentions = data.get('dimentions') or []
        self.children = data.get('children') or []
        self.params_types = data.get('params_types') or []
        self.rtype = data.get('return_type') or 'vazio'

        self.__reduced = False
        self.__data['id'] = str(Base.__id)

        Base.__id += 1
        

    def __repr__(self):
        return f"{self.id}"

        # representation = f"{self.id}"
        # if self.is_function():
        #     representation += "  --> FUNCTION"
        # elif self.is_variable():
        #     representation += "  --> VARIABLE"

        # if self.scope:
        #     representation += f"\n\tSCOPE: {self.scope}"
        # if self.operation:
        #     representation += f"\n\tOPERATION: {self.operation}"
        # if self.visible_scopes:
        #     representation += f"\n\tVISIBLE_SCOPES: {str(self.type)}"
        # if self.dimentions:
        #     representation += f"\n\tDIMENTIONS: {str([item.get('size') for item in self.dimentions])}"
        # if self.rtype:
        #     representation += f"\n\tRETURN_TYPE: {self.rtype}"

        # representation += f"\n\tCHILDREN: {[str(item) for item in self.children]}"

        # if self.params_types:
        #     representation += f"\n\PARAMS: {str([item.get('type') for item in self.params_types])}"

        # return representation

    def __str__(self):
        return f"{self.id}"

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

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
            if name == 'return_type' and self.__data.get(name) == None:
                return self.__type__()
            return self.__data.get(name)
        return _get

    def __del__(name):
        def _del(self):
            del self.__data[name]
        return _del

    def __type__(self):
        self.__data['return_type'] = 'vazio'
        return 'vazio'


    def insert_node_below(self, node):
        if type(node) is list:
            for node_adj in node:
                node_adj.scope = self.scope
                self.insert_node_below(node_adj)
        else:
            self.children = self.children + [node]
        pass

    def is_variable(self):
        return self.__data.get('variable') or False

    def is_function(self):
        return self.__data.get('callable') or False

    def graphic_repr(self, graph=None):
        if not graph:
            graph = Base.__digraph

        graph.node(self.graph_id, self.id)

        for adj in self.children:
            adj.graphic_repr(graph)
            graph.edge(self.graph_id, adj.graph_id, constraint='true')

        return graph

    def reduce(self, debug=False):
        pass

    def semantic_a(self, debug=False):
        pass

    def generator(self, builder, debug=False):
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

    id = property(__get__('identifier'))

    graph_id = property(__get__('id'))

    children = property(__get__('children'), __set__(
        'children'), __del__('children'))

    params_types = property(__get__('params_types'), __set__(
        'params_types'), __del__('params_types'))

    value = property(__get__('value'), __set__('value'), __del__('value'))

    intable = property(__get__('table'), __set__('table'), __del__('table'))

