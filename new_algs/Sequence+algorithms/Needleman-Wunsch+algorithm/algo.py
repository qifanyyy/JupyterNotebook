import numpy
import warnings
from typing import List, Any, Tuple, Dict
from .utils import Config


class NWAlgo:
    def __init__(self, config: Config):
        self._config = config

    def compute_cost_matrix(self, first_seq: str, second_seq: str) -> Any:
        cost_matrix = numpy.zeros(((len(first_seq) + 1, len(second_seq) + 1)))
        for i in range(1, (len(first_seq) + 1)):
            cost_matrix[i, 0] = i * self._config.gap
        for i in range(1, (len(second_seq)) + 1):
            cost_matrix[0, i] = i * self._config.gap

        for i in range(1, (len(first_seq) + 1)):
            for j in range(1, (len(second_seq) + 1)):
                left = cost_matrix[i, j - 1] + self._config.gap
                up = cost_matrix[i - 1, j] + self._config.gap
                comp = (
                    self._config.same
                    if first_seq[i - 1] == second_seq[j - 1]
                    else self._config.diff
                )
                diag = cost_matrix[i - 1, j - 1] + comp
                cost_matrix[i, j] = max(left, up, diag)

        return cost_matrix

    def get_all_alignments(self, first_seq: str, second_seq: str, cost_matrix: Any):
        graph = self._retrieve_previous_nodes(first_seq, second_seq, cost_matrix)
        paths = self._find_all_paths(
            graph, (len(first_seq), len(second_seq)), (0, 0), list()
        )
        alignments: List[Tuple[str, str]] = list()
        for path in paths:
            first_aligned = ""
            second_aligned = ""
            previous_node = (len(first_seq), len(second_seq))

            for current_node in path[1:]:
                i, j = previous_node
                if i == current_node[0]:
                    first_aligned = "-" + first_aligned
                    second_aligned = second_seq[j - 1] + second_aligned
                elif j == current_node[1]:
                    first_aligned = first_seq[i - 1] + first_aligned
                    second_aligned = "-" + second_aligned
                else:
                    first_aligned = first_seq[i - 1] + first_aligned
                    second_aligned = second_seq[j - 1] + second_aligned

                previous_node = current_node

            alignments += [(first_aligned, second_aligned)]

        return alignments

    def _retrieve_previous_nodes(
        self, first_seq: str, second_seq: str, cost_matrix: Any
    ):
        graph = dict()
        for i in range(len(first_seq), 0, -1):
            graph[(i, 0)] = [(i - 1, 0)]
            graph[(0, i)] = [(0, i - 1)]

            for j in range(len(second_seq), 0, -1):
                graph[(i, j)] = list()
                left = cost_matrix[i, j - 1] + self._config.gap
                up = cost_matrix[i - 1, j] + self._config.gap
                comp = (
                    self._config.same
                    if first_seq[i - 1] == second_seq[j - 1]
                    else self._config.diff
                )
                diag = cost_matrix[i - 1, j - 1] + comp
                if cost_matrix[i, j] == left:
                    graph[(i, j)] += [(i, j - 1)]
                if cost_matrix[i, j] == up:
                    graph[(i, j)] += [(i - 1, j)]
                if cost_matrix[i, j] == diag:
                    graph[(i, j)] += [(i - 1, j - 1)]

        return graph

    def _find_all_paths(
        self,
        graph: Dict[Tuple[int, int], List[Tuple[int, int]]],
        start: Tuple[int, int],
        end: Tuple[int, int],
        path: List[Tuple[int, int]],
    ) -> List[List[Tuple[int, int]]]:
        path = path + [start]
        if start == end:
            return [path]
        elif start not in graph:
            return list()

        paths: List[List[Tuple[int, int]]] = list()
        for node in graph[start]:
            if node not in path:
                new_paths = self._find_all_paths(graph, node, end, path)
                if len(paths) + len(new_paths) > self._config.max_paths:
                    warnings.warn(
                        f"Too many paths found. Returning top {self._config.max_paths}",
                        stacklevel=2,
                    )
                    return paths
                else:
                    paths += new_paths

        return paths
