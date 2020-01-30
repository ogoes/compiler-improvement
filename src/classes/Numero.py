from classes.Base import Base


class Numero(Base):

    def __init__(self, **data):
        data['identifier'] = 'NUMERO'
        
        super().__init__(data)

    def graphic_repr(self, graph=None):

        if graph:
            leaf = self.graph_id + str(float(self.value))

            graph.node(self.graph_id, self.id)
            graph.node(leaf, label=self.value)

            graph.edge(self.graph_id, leaf, constraint='true')

            return graph
