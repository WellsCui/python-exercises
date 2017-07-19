import unittest

import numpy as np

import org.wells.graphlib as graphlib


class MazeGraph(graphlib.IGraph):
    def __init__(self, maze, rows, cols):
        self.maze = maze
        self.rows = rows
        self.cols = cols

    def __get_adjacent_nodes(self, node):
        if node[1] == 0 and node[0] == 0:
            return [[0, 1], [1, 0]]
        elif node[1] == 0 and node[0] > 0 and (node[0] < self.rows - 1):
            return [[node[0] - 1, 0], [node[0] + 1, 0], [node[0], 1]]
        elif node[1] == 0 and node[0] == self.rows - 1:
            return [[node[0] - 1, 0], [node[0], 1]]
        elif node[0] == self.rows - 1 and node[1] > 0 and (node[1] < self.cols - 1):
            return [[node[0], node[1] - 1], [node[0], node[1] + 1], [node[0] - 1, node[1]]]
        elif node[0] == self.rows - 1 and node[1] == self.cols - 1:
            return [[node[0], node[1] - 1], [node[0] - 1, node[1]]]
        elif node[1] == self.cols - 1 and node[0] > 0 and (node[0] < self.rows - 1):
            return [[node[0], node[1] - 1], [node[0] - 1, node[1]], [node[0] + 1, node[1]]]
        elif node[1] == self.cols - 1 and node[0] == 0:
            return [[0, node[1] - 1], [node[0] + 1, node[1]]]
        elif node[1] < self.cols - 1 and node[0] == 0:
            return [[0, node[1] - 1], [0, node[1] + 1], [node[0] + 1, node[1]]]
        else:
            return [[node[0], node[1] - 1], [node[0], node[1] + 1],
                    [node[0] - 1, node[1]], [node[0] + 1, node[1]]]

    def get_links(self, node):
        adjacent_nodes = self.__get_adjacent_nodes(node)
        return (node for node in adjacent_nodes if self.maze[node[0], node[1]] == 0)


class MazeNodeVisitor(graphlib.INodeVisitor):
    def __init__(self, exit_node, ended_when_found):
        self.exit_node = exit_node
        self.ended_when_found = ended_when_found

    def visit(self, graph: graphlib.IGraph, node, path, context):
        print('visiting node:', node, ' with path:', path)
        if node == self.exit_node:
            context["ended"] = self.ended_when_found
            context["paths"].append(path)
            return False
        return True


def walk_maze_graph(graph: MazeGraph, start_node, exit_node):
    context = {"ended": False,
               "paths": []}
    walker = graphlib.BreadthFirstGraphWalker(MazeNodeVisitor(exit_node, True), lambda ctx: ctx["ended"])
    walker.walk(graph, start_node, context)
    return context["paths"]


def gaussian_distance(node1, node2):
    return ((node1[0]-node2[0])**2+(node1[1]-node2[1])**2)**0.5


def depth_first_walk_maze_graph(graph: MazeGraph, start_node, exit_node):
    context = {"ended": False,
               "paths": []}
    walker = graphlib.DepthFirstGraphWalker(MazeNodeVisitor(exit_node, True), lambda ctx: ctx["ended"], False)
    walker.walk(graph, start_node, context)
    return context["paths"]


def heuristic_walk_maze_graph(graph: MazeGraph, start_node, exit_node):
    context = {"ended": False,
               "paths": []}
    heuristic_fn = (lambda node: gaussian_distance(node, exit_node))
    walker = graphlib.HeuristicGraphWalker(MazeNodeVisitor(exit_node, True), lambda ctx: ctx["ended"], heuristic_fn)
    walker.walk(graph, start_node, context)
    return context["paths"]


def find_all_maze_paths(graph: MazeGraph, start_node, exit_node):
    context = {"ended": False,
               "paths": []}

    walker = graphlib.DepthFirstGraphWalker(MazeNodeVisitor(exit_node, False), lambda ctx: ctx["ended"], False)
    walker.walk(graph, start_node, context)
    return context["paths"]


def find_shortest_maze_path(maze, rows, cols, start_rows, start_col, exit_row, exit_col):
    graph = MazeGraph(maze, rows, cols)
    return walk_maze_graph(graph, [start_rows, start_col], [exit_row, exit_col])


class MazeTest(unittest.TestCase):

    def test_find_shortest_maze_path(self):
        maze = np.array([[0, 1, 0, 0, 0],
                         [0, 0, 1, 0, 1],
                         [1, 0, 0, 0, 0],
                         [0, 1, 1, 0, 1],
                         [0, 0, 0, 0, 0]])
        expected_path = [[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [3, 3], [4, 3], [4, 2], [4, 1]]]

        path = find_shortest_maze_path(maze, 5, 5, 0, 0, 4, 1)
        print("shortest path:", path)
        self.assertEqual(expected_path, path)

    def test_heuristic_walk_maze_graph(self):
        maze = np.array([[0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0],
                         [0, 1, 1, 0, 1],
                         [0, 0, 0, 0, 0]])
        graph = MazeGraph(maze, 5, 5)
        heuristic_path = heuristic_walk_maze_graph(graph, [1,1], [4, 4])
        print("heuristic path:", heuristic_path)
        shortest_path = walk_maze_graph(graph, [1, 1], [4, 4])
        print("stortest path:", shortest_path)
        depth_first_path = depth_first_walk_maze_graph(graph, [1, 1], [4, 4])
        print("depth first path:", depth_first_path)

    def test_find_all_maze_paths(self):
        maze = np.array([[0, 1, 0, 0, 0],
                         [0, 0, 1, 0, 1],
                         [1, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0]])
        expected_path = [[[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [4, 1], [4, 2]],
                         [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1], [3, 0], [4, 0], [4, 1], [4, 2]],
                         [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [3, 3], [4, 3], [4, 2]],
                         [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [3, 3], [3, 4], [4, 4], [4, 3], [4, 2]],
                         [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4], [4, 4], [4, 3], [4, 2]],
                         [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 2]]]

        graph = MazeGraph(maze, 5, 5)
        paths = find_all_maze_paths(graph, [0, 0], [4, 2])
        self.assertEqual(len(list(path for path in paths if path in expected_path)), len(expected_path))
        self.assertEqual(len(paths), len(expected_path))


if __name__ == '__main__':
    unittest.main()

