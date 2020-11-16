import pytest
import bioinfnw.utils as utils
import bioinfnw.algo as algo


def test_compute_cost_matrix_simple():
    config = utils.Config(5, -5, -2, 99, 9999)
    a = "SAM"
    b = "SUM"
    algo_instance = algo.NWAlgo(config)

    cost_matrix = algo_instance.compute_cost_matrix(a, b)

    assert cost_matrix[len(a), len(b)] == 6


def test_compute_cost_matrix_advanced():
    config = utils.Config(5, -5, -2, 99, 9999)
    a = "GAAC"
    b = "CAAGAC"
    algo_instance = algo.NWAlgo(config)

    cost_matrix = algo_instance.compute_cost_matrix(a, b)

    assert cost_matrix[len(a), len(b)] == 7


def test_retrieve_previous_nodes():
    config = utils.Config(5, -5, -2, 99, 9999)
    a = "SAM"
    b = "SUM"
    algo_instance = algo.NWAlgo(config)
    cost_matrix = algo_instance.compute_cost_matrix(a, b)

    graph = algo_instance._retrieve_previous_nodes(a, b, cost_matrix)

    assert graph[(3, 2)] == [(3, 1), (2, 2)]


def test_find_all_paths():
    config = utils.Config(5, -5, -2, 99, 9999)
    a = "SAM"
    b = "SUM"
    algo_instance = algo.NWAlgo(config)
    cost_matrix = algo_instance.compute_cost_matrix(a, b)
    graph = algo_instance._retrieve_previous_nodes(a, b, cost_matrix)

    paths = algo_instance._find_all_paths(graph, (len(a), len(b)), (0, 0), list())
    assert paths == [
        [(3, 3), (2, 2), (2, 1), (1, 1), (0, 0)],
        [(3, 3), (2, 2), (1, 2), (1, 1), (0, 0)],
    ]


@pytest.mark.filterwarnings("ignore:Too many paths found")
def test_find_all_paths_truncated():
    config = utils.Config(5, -5, -2, 1, 9999)
    a = "SAM"
    b = "SUM"
    algo_instance = algo.NWAlgo(config)
    cost_matrix = algo_instance.compute_cost_matrix(a, b)
    graph = algo_instance._retrieve_previous_nodes(a, b, cost_matrix)

    paths = algo_instance._find_all_paths(graph, (len(a), len(b)), (0, 0), list())
    assert paths == [
        [(3, 3), (2, 2), (2, 1), (1, 1), (0, 0)],
    ]


def test_get_all_alignments():
    config = utils.Config(5, -5, -2, 99, 9999)
    a = "SAM"
    b = "SUM"
    algo_instance = algo.NWAlgo(config)
    cost_matrix = algo_instance.compute_cost_matrix(a, b)

    alignments = algo_instance.get_all_alignments(a, b, cost_matrix)

    assert alignments == [("SA-M", "S-UM"), ("S-AM", "SU-M")]
