from abc import ABCMeta, abstractmethod


class IGraph(metaclass=ABCMeta):
    @abstractmethod
    def get_links(self, node):
        pass


class IGraphWalker(metaclass=ABCMeta):
    @abstractmethod
    def walk(self, graph: IGraph, node, context):
        pass


class INodeVisitor(metaclass=ABCMeta):
    @abstractmethod
    def visit(self, graph: IGraph, node, path, context):
        pass


def get_filtered_linked_nodes(graph, node, excluded):
    return (linked for linked in graph.get_links(node) if (linked not in excluded))


class BreadthFirstGraphWalker(IGraphWalker):
    def __init__(self, node_visitor: INodeVisitor, is_walk_ended):
        self.node_visitor = node_visitor
        self.is_walk_ended = is_walk_ended

    def walk(self, graph: IGraph, node, context):
        visiting = [[node, [node]]]
        visited = []
        while len(visiting) > 0 and not self.is_walk_ended(context):
            visiting_node_info = visiting.pop(0)
            visiting_node = visiting_node_info[0]
            path = visiting_node_info[1]
            visited.append(visiting_node)
            if self.node_visitor.visit(graph, visiting_node, path, context):
                linked_nodes = get_filtered_linked_nodes(graph,
                                                           visiting_node,
                                                           visited +
                                                           list(item for item, _ in visiting))

                visiting = visiting + list([linked, path+[linked]] for linked in linked_nodes)


class DepthFirstGraphWalker(IGraphWalker):
    def __init__(self, node_visitor: INodeVisitor, is_walk_ended, revisit_enabled: bool):
        self.node_visitor = node_visitor
        self.is_walk_ended = is_walk_ended
        self.revisit_enabled = revisit_enabled

    def walk(self, graph: IGraph, node, context):
        visiting = [[node, [node]]]
        while len(visiting) > 0 and not self.is_walk_ended(context):
            visiting_node_info = visiting.pop()
            visiting_node = visiting_node_info[0]
            path = visiting_node_info[1]

            if self.node_visitor.visit(graph, visiting_node, path, context):
                excluded_nodes = [node]
                if not self.revisit_enabled:
                    excluded_nodes = path
                linked_nodes = get_filtered_linked_nodes(graph, visiting_node, excluded_nodes)
                visiting = visiting + list([linked, path+[linked]] for linked in linked_nodes)


class HeuristicGraphWalker(IGraphWalker):
    def __init__(self, node_visitor: INodeVisitor, is_walk_ended, heuristic_fn):
        self.node_visitor = node_visitor
        self.is_walk_ended = is_walk_ended
        self.heuristic_fn = heuristic_fn

    @staticmethod
    def __sort_visiting(visiting):
        visiting.sort(key=lambda visiting_node_info: visiting_node_info[2])

    def walk(self, graph: IGraph, node, context):
        visiting = [[node, [node], self.heuristic_fn(node)]]
        while len(visiting) > 0 and not self.is_walk_ended(context):
            visiting_node_info = visiting.pop(0)
            visiting_node = visiting_node_info[0]
            path = visiting_node_info[1]

            if self.node_visitor.visit(graph, visiting_node, path, context):
                linked_nodes = get_filtered_linked_nodes(graph, visiting_node, path)
                linked_visiting = list([linked, path+[linked], self.heuristic_fn(linked)] for linked in linked_nodes)
                visiting = visiting + linked_visiting
                self.__sort_visiting(visiting)
