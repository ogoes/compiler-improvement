from classes.Base import Base


class Tipo(Base):

    def __init__(self, **data):
        data['identifier'] = 'TIPO'

        super().__init__(data)

    def graphic_repr(self, graph=None):
        

        if graph:
            leaf = self.graph_id + self.rtype

            graph.node(self.graph_id, self.id)
            graph.node(leaf, label=self.rtype.upper())

            graph.edge(self.graph_id, leaf, constraint='true')

            return graph
