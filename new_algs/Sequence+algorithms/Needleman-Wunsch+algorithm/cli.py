import click
from bioinfnw.utils import Config, read_config_file, read_fasta_file, write_alignments
from bioinfnw.algo import NWAlgo


@click.command()
@click.option("-a", type=click.Path(exists=True))
@click.option("-b", type=click.Path(exists=True))
@click.option("-c", type=click.Path(exists=True))
@click.option("-o")
def calculate_alignment(a: str, b: str, c: str, o: str):
    first_seq = read_fasta_file(a)
    second_seq = read_fasta_file(b)

    config = read_config_file(c)
    if (
        len(first_seq) > config.max_sequence_length
        or len(second_seq) > config.max_sequence_length
    ):
        raise ValueError("Too long sequences to analyze")

    algo = NWAlgo(config)

    cost_matrix = algo.compute_cost_matrix(first_seq, second_seq)
    alignments = algo.get_all_alignments(first_seq, second_seq, cost_matrix)

    write_alignments(o, int(cost_matrix[len(first_seq), len(second_seq)]), alignments)


if __name__ == "__main__":
    calculate_alignment()
