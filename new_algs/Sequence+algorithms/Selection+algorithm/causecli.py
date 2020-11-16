#!/usr/bin/env python3
import click
import numpy as np

from cause.preprocessor import RawStatsLoader
from cause.preprocessor import RawSampleStatsLoader
from cause.preprocessor import FeatureExtractor
from cause.preprocessor import DatasetCreator
from cause.preprocessor import SamplesDatasetCreator
from cause.preprocessor import SampleStatsFit

from cause.stats import ProcessedDataset
from cause.stats import ProcessedSamplesDataset

from cause.features import Features
from cause.malaise import MALAISEPredictor
from cause.praise import PRAISEPredictor

from cause.postprocessor import Postprocessor
from cause.postprocessor import FeatsPostprocessor
from cause.postprocessor import MALAISEPostprocessor
from cause.postprocessor import PRAISEPostprocessor


def validate_weights(ctx, param, value):
    # domain = None --> return None
    # domain != None --> validate domain: list of floats>0

    if value is None:
        return None

    def positive_float(f):
        if float(f) < 0:
            raise ValueError(None)
        else:
            return float(f)

    try:
        return np.array([positive_float(x) for x in value.split(",")])
    except ValueError:
        raise click.BadParameter('%s should be a comma-separated list of floats >= 0, not \'%s\'' % (param.name, value))


@click.group()
def cli():
    pass


# compare all
# compare stochastic

@cli.group(short_help='subcommand to compare algorithms', name='compare')
def compare():
    pass


@compare.command(short_help='compare all algorithms w.r.t optimal', name='all')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def cmp_all(name, infolder, outfolder):
    """Loads raw stats in INFOLDER obtained by running the portfolio on
    the dataset NAME and then plots time and welfare of each algorithm w.r.t.
    the time and welfare of the optimal algorithm.
    The plots are saved to OUTFOLDER.
    """
    RawStatsLoader(infolder, name).load_optimal().plot(outfolder)


@compare.command(short_help='compare all stochastic algorithms', name='stochastic')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def cmp_rand(name, infolder, outfolder):
    """Loads raw stats in INFOLDER obtained by running the portfolio on
    the dataset NAME and then plots welfare of stochastic algorithms over
    multiple runs, w.r.t. the average value for each instance.
    The plots are saved to OUTFOLDER.
    """
    RawStatsLoader(infolder, name).load_random().plot(outfolder)


# preprocess features
# preprocess stats
# preprocess samples

@cli.group(short_help='subcommand to preprocess collected raw data', name='preprocess')
def preprocess():
    pass


@preprocess.command(short_help='extract features from auction instances', name='features')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def preproc_features(instance_folder, name, outfolder):
    """Extracts features of auction instances in INFOLDER comprising dataset NAME
    and saves them to OUTFOLDER using the given name.
    """
    FeatureExtractor.extract(instance_folder, name, outfolder)


@preprocess.command(short_help='extract and compute, then save algorithm stats on full instances',
                    name='stats')
@click.option("--weights", callback=validate_weights,
              default='0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.',
              help='lambda weights for the cost model (float or list of floats)')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def preproc_stats(name, weights, infolder, outfolder):
    """Processes raw stats in INFOLDER obtained by running the heuristic algorithms
    in algorithm portfolio on dataset NAME, and saves them to OUTFOLDER
    using the given name.

    The weights used in the cost model to determine the best algorithm are passed
    as a comma-separated list of positive floats (or a single value), with the
    default value: '0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.'.
    """
    DatasetCreator.create(weights, infolder, outfolder, name)


@preprocess.command(short_help='extract and compute, then save algorithm stats on instance samples',
                    name='samples')
@click.option("--weights", callback=validate_weights,
              default='0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.',
              help='lambda weights for the cost model (float or list of floats)')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def preproc_samples(name, weights, infolder, outfolder):
    """Processes raw stats in INFOLDER obtained by running the heuristic algorithms
    in algorithm portfolio on samples of each instance in the dataset NAME,
    and saves them to OUTFOLDER using the given name.

    The weights used in the cost model to determine the best algorithm are passed
    as a comma-separated list of positive floats (or a single value), with the
    default value: '0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.'.
    """
    SamplesDatasetCreator.create(weights, infolder, outfolder, name)


# run malaise
# run praise
# run fitting

@cli.group(short_help='subcommand to run algorithm selection', name='run')
def run():
    pass


@run.command(short_help='run MALAISE', name='malaise')
@click.option("--weights", callback=validate_weights,
              default='0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.',
              help='lambda weights for the cost model (float or list of floats)')
@click.option("--nthreads", type=int, default=1,
              help='number of threads for parallel training with auto-sklearn')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def run_malaise(name, weights, infolder, outfolder, nthreads):
    """Runs MALAISE algorithm selection on dataset NAME, with processed stats
    and extracted features located in INFOLDER. The trained models and evaluation
    results (accuracy and MSE error) are saved to OUTFOLDER, as well as results
    for random selection and best algorithm selection, to be used for comparison.

    The training uses auto-ml to find the best hyperparameters, and it can be
    done in parallel if nthreads are given.

    The weights used in the cost model to determine the best algorithm are passed
    as a comma-separated list of positive floats (or a single value), with the
    default value: '0.,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.'.
    """
    # load processed features
    feats = Features.load("%s/%s_features.yaml" % (infolder, name))
    # load processed dataset
    ds = ProcessedDataset.load("%s/%s.yaml" % (infolder, name))
    # run MALAISE for each given weight
    for weight in ds.weights:
        MALAISEPredictor(ds.lstats[weight], feats).run(
            outfolder=outfolder, num_processes=nthreads)


@run.command(short_help='run PRAISE', name='praise')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def run_praise(name, infolder, outfolder):
    """Runs PRAISE algorithm selection on dataset NAME, with processed stats
    and sample stats located in INFOLDER. The evaluation results (accuracy and
    MSE error) are saved to OUTFOLDER, as well as results for random selection
    and best algorithm selection, to be used for comparison.

    The weights used in the cost model to determine the best algorithm, as well
    as the sampling ratios, are taken from the processed stats.
    """
    ## load samples dataset
    sds = ProcessedSamplesDataset.load("%s/%s_samples.yaml" % (infolder, name))
    ## load full instance dataset
    fds = ProcessedDataset.load("%s/%s.yaml" % (infolder, name))
    ## run PRAISE on all lambda weights
    for weight in fds.weights:
        for ratio in sds.ratios:
            PRAISEPredictor(
                fds.pstats, fds.lstats[weight],
                sds.sstats[ratio], sds.lstats[ratio][weight]
                ).run(outfolder=outfolder)


@run.command(short_help='curve fitting for scaling behavior over problem size',
             name='fitting')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def run_fitting(name, infolder, outfolder):
    """Given the raw sample stats in INFOLDER (time and welfare computed by the
    algorithms over multiple sample sizes, on the dataset given by NAME), it
    performs curve fitting for multiple functions to determine scaling behavior
    of each algorithm for time and welfare over problem size.
    The results are printed to standard output.
    """
    allstats = RawSampleStatsLoader(infolder, name).load()
    SampleStatsFit.fit_welfare(allstats)
    SampleStatsFit.fit_time(allstats)


# postprocess breakdown
# postprocess features
# postprocess malaise
# postprocess praise

@cli.group(short_help='subcommand to postprocess algorithm selection results',
           name='postprocess')
def postprocess():
    pass


@postprocess.command(short_help='get dataset breakdown by best algorithm', name='breakdown')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def postprocess_breakdown(name, infolder, outfolder):
    """Takes preprocessed stats in INFOLDER given by NAME, and breaks down the
    dataset based on the best algorithms, for each lambda weight.
    The breakdown is then saved to OUTFOLDER using the given name, as a heatmap
    image, as well as a text file in tabular format.
    """
    # load processed dataset
    ds = ProcessedDataset.load("%s/%s.yaml" % (infolder, name))
    ## get breakdown by algorithms and weights
    breakdown = Postprocessor(ds).breakdown()
    ## save to file for latex table
    breakdown.save_to_latex(outfolder)
    ## plot breakdown as heatmap
    breakdown.plot(outfolder)


@postprocess.command(short_help='get feature importances', name='features')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def postprocess_features(name, infolder, outfolder):
    """Takes preprocessed stats and extracted features in INFOLDER,
    given by the dataset's NAME, and computes the feature importances using
    tree-based classifiers, for each lambda weight, as well as on average over
    lambda.
    The importances are then saved to OUTFOLDER using the given name, as text
    files in tabular format. A feature heatmap expressing correlations between
    features is also created.
    """
    # load processed features
    feats = Features.load("%s/%s_features.yaml" % (infolder, name))
    # load processed stats
    ds = ProcessedDataset.load("%s/%s.yaml" % (infolder, name))
    ## postprocessing: feature importances
    fpostp = FeatsPostprocessor(ds, feats)
    fpostp.save_feature_importances(outfolder)
    for weight in ds.weights:
        fpostp.save_feature_importances_by_weight(outfolder, weight)
    ## plot features as heatmap
    feats.plot(outfolder)


@postprocess.command(short_help='postprocess MALAISE results', name='malaise')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def postprocess_malaise(name, infolder, outfolder):
    """Takes the results of running MALAISE on dataset NAME, saved in INFOLDER,
    and saves the accuracy and RMSE values over lambda to OUTFOLDER,
    using the given name, as text files in tabular format.
    """
    MALAISEPostprocessor("%s/%s_stats" % (infolder, name)).save(outfolder)


@postprocess.command(short_help='postprocess PRAISE results', name='praise')
@click.argument("name")
@click.argument("infolder", type=click.Path(exists=True))
@click.argument("outfolder", type=click.Path(exists=True))
def postprocess_praise(name, infolder, outfolder):
    """Takes the results of running PRAISE on dataset NAME, saved in INFOLDER,
    and saves the accuracy and RMSE values over lambda to OUTFOLDER,
    using the given name, as text files in tabular format.
    """
    PRAISEPostprocessor("%s/%s_stats" % (infolder, name)).save(outfolder)


if __name__ == '__main__':
    cli()
