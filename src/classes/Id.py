from classes.Base import Base


class Id(Base):
    def __init__(self, **data):
        super().__init__(data)

    def graphic_repr(self, graph=None):
        
        if graph:
            leaf = self.graph_id + self.id

            graph.node(self.graph_id, 'ID')
            graph.node(leaf, label=self.id)

            graph.edge(self.graph_id, leaf, constraint='true')

            return graph
