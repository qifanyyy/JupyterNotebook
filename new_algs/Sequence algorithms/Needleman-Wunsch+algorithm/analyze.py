import click
from SequenceAnalyzer import SequencesAnalyzer
from HirschbergAlgorithm import HirschbergAlgorithm
from ScoringSystem import ScoringSystem

@click.command()
@click.argument('sequence_a')
@click.argument('sequence_b')
@click.option('-S', '--summary', is_flag=True)
@click.option('-s', '--similarity', is_flag=True)
@click.option('-e', '--edit-distance', is_flag=True)
@click.option('-a', '--alignment', type=click.Choice(['global', 'local']))
#@click.option('--load', type=click.Path(exists=True), help='Text file containing 5x5 matrix of integers separated by spaces and new line')
@click.option('--load-csv', is_flag=True, help='Load scores.csv and edit_cost.csv')
def main(load_csv, summary, similarity, edit_distance, sequence_a, sequence_b, alignment):
    analyzer = SequencesAnalyzer(sequence_a, sequence_b, load_csv=load_csv)

    if summary:
        analyzer.edit_distance()
        analyzer.similarity()
        analyzer.local_alignment()
        analyzer.global_alignment()
    if similarity:
        analyzer.similarity()
    if edit_distance:
        analyzer.edit_distance()

    if alignment == 'local':
        analyzer.local_alignment()
    elif alignment == 'global':
        analyzer.global_alignment()
        print('--------------------------')
        #analyzer.hirschberg_algorithm(X=analyzer.seq_a, Y=analyzer.seq_b)
        scoring_sys = ScoringSystem(match=2, mismatch=-1, gap=-2)
        HirschbergAlgorithm(scoring_sys).align(sequence_a, sequence_b)


if __name__ == '__main__':
    main()
