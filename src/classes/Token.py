from classes.Base import Base


class Token(Base):
    def __init__(self, **data):

        self.label = 'TOKEN'

        super().__init__(data)

    def graphic_repr(self, graph=None):
        
        if graph:
            leaf = self.graph_id + 'tok'

            graph.node(self.graph_id, 'TOKEN')
            graph.node(leaf, label=self.id)

            graph.edge(self.graph_id, leaf, constraint='true')

            return graph
