

from classes.Base import Base


class Operator(Base):
    def __init__(self, data):
        self.label = 'OPERATOR'
        super().__init__(data)


    def graphic_repr(self, graph=None):
        if not graph:
            graph = Base.__digraph

        leaf = self.graph_id + self.id

        graph.node(self.graph_id, self.label)
        graph.node(leaf, self.id)


        children = [leaf]

        if self.children:
            left_child = self.children[0]
            right_child = self.children[1]

            left_child.graphic_repr(graph)
            right_child.graphic_repr(graph)

            children = [left_child.graph_id] + children
            children = children + [right_child.graph_id]

        for node in children:
            graph.edge(self.graph_id, node, constraint='true')


        return graph
