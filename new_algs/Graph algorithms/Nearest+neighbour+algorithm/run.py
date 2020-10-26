import sys
import pandas as pd
from scripts.wekaloader import start_weka, stop_weka, load_Arff_file
from scripts.clustering import run_clusterer
from scripts.bayes_networks import run_bayesNet
from scripts.naiveBayes import run_naiveBayes
from scripts.multilayer_percepton import run_multilayerPercepton
from weka.classifiers import Classifier, Evaluation, PredictionOutput
from weka.core.classes import Random
from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
from config import data_dirs, data_files, data_dirs3, data_dirs3_appended, data_files3
from helper import randomise_CSV, splitTestingSets, to_ARFF, output_eval, output_pred, get_ARFFs_in_dir, get_CSVs_in_dir, output_select_attribute
import time


Field2 = []
Field5 = []
Field10 = []
Field50 = []
a = 0


def init():
    try:
        # Start Javabridge
        start_weka()

        while True:
            # Match with if's below
            print("\nSelect Options to proceed:")
            print("1 : Randomise CSV's")
            print("2 : Run IBk algorithm")
            print("3 : Select Attribute Creation")
            print("4 : Run Bayes Net")
            print("5 : Run Clusterer")
            print("6 : Run Naive Bayes")
            print("7 : Split file into testing set")
            print("8 : Run Multilayer Percepton")
            print("0 : End Program")

            x = int(input())

            if x == 1:
                make_dirs3()
                make_random_CSVs()
            elif x == 2:
                for dirs in data_dirs:
                    if dirs == "root":
                        continue
                    for file in get_ARFFs_in_dir(data_dirs[dirs]):
                        start = time.time()
                        print("IBk run time for file: %s", str(file))
                        run_ibk(file)
                        end = time.time()
                        timetaken = round(end - start, 2)
                        print("Time taken to run: %s seconds" % (timetaken))
            elif x == 3:
                for dirs in data_dirs3_appended:
                    if dirs == "root":
                        continue
                    for file in get_ARFFs_in_dir(data_dirs3_appended[dirs]):
                        select_attribute(file)
                    make_CSV_SA(
                        data_dirs3_appended[dirs] / "fer2018_main.csv")
            elif x == 4:
                for dirs in data_dirs:  # Loops through all data dirs
                    if dirs == "root":
                        continue
                    for file in get_ARFFs_in_dir(data_dirs[dirs]):
                        # Only gets main files
                        if file.name.endswith("fer2018_main.arff") or file.name.endswith("Field.arff"):
                                # Only gets main files
                            start = time.time()
                            print("bayesNet run time for file: %s", str(file))
                            run_bayesNet(file)
                            end = time.time()
                            timetaken = round(end - start, 2)
                            print("Time taken to run: %s seconds" %
                                  (timetaken))

            elif x == 5:
                for dirs in data_dirs:  # Loops through all data dirs
                    if dirs == "root":
                        continue
                    for file in get_ARFFs_in_dir(data_dirs[dirs]):
                        # Only gets main files
                        if file.name.endswith("_main.arff"):
                            start = time.time()
                            print("Cluster run time for file: %s", str(file))
                            run_clusterer(file)
                            end = time.time()
                            timetaken = round(end - start, 2)
                            print("Time taken to run: %s seconds" %
                                  (timetaken))

            elif x == 6:
                for dirs in data_dirs:  # Loops through all data dirs
                    if dirs == "root":
                        continue
                    for file in get_ARFFs_in_dir(data_dirs[dirs]):
                        # Only gets main files
                        if file.name.endswith("fer2018_main.arff") or file.name.endswith("Field.arff"):
                            run_naiveBayes(file)
            elif x == 7:
                make_dirs3()
                make_training_set()
            elif x == 8:
                for dirs in data_dirs3_appended:  # Loops through all data dirs
                    if dirs == "root":
                        continue
                    print(data_dirs3_appended[dirs])
                    ARFFs = get_ARFFs_in_dir(data_dirs3_appended[dirs])
                    print(ARFFs)
                    if ARFFs[0].name.startswith("fer2017-training"):
                        train = ARFFs[0]
                        test = ARFFs[1]
                    else:
                        train = ARFFs[1]
                        test = ARFFs[0]
                    print("Training on " + train.name +
                          " and testing on " + test.name)
                    run_multilayerPercepton(train, test)

            elif x == 0:
                print("Exiting")
                stop_weka()
                sys.exit(0)
            else:
                print("Input %d not valid." % x)

    except Exception as e:
        print(e)
    finally:
        stop_weka()


def make_CSV_SA(file):
    # Output directory
    data_dir = file.parents[0]
    name = file.name[:-5]

    f = pd.read_csv(file)
    keep_col_2Field = ['emotion']
    keep_col_5Field = ['emotion']
    keep_col_10Field = ['emotion']
    keep_col_50Field = ['emotion']

    print(str(len(Field2)))
    for i in range(len(Field2)):
        keep_col_2Field.append('pixel' + str(Field2[i]))
    new_f = f[keep_col_2Field]
    new_f.to_csv(data_dir / (name + "_2Field.csv"), index=False)

    print(str(len(Field5)))
    for i in range(len(Field5)):
        keep_col_5Field.append('pixel' + str(Field5[i]))
    new_f = f[keep_col_5Field]
    new_f.to_csv(data_dir / (name + "_5Field.csv"), index=False)

    print(str(len(Field10)))
    for i in range(len(Field10)):
        keep_col_10Field.append('pixel' + str(Field10[i]))
    new_f = f[keep_col_10Field]
    new_f.to_csv(data_dir / (name + "_10Field.csv"), index=False)

    print(str(len(Field50)))
    for i in range(len(Field50)):
        keep_col_50Field.append('pixel' + str(Field50[i]))
    new_f = f[keep_col_50Field]
    new_f.to_csv(data_dir / (name + "_50Field.csv"), index=False)

    to_ARFF(data_dir / (name + "_2Field.csv"))
    to_ARFF(data_dir / (name + "_5Field.csv"))
    to_ARFF(data_dir / (name + "_10Field.csv"))
    to_ARFF(data_dir / (name + "_50Field.csv"))


def select_attribute(file):
    global Field50
    global Field10
    global Field5
    global Field2
    global a

    filename = file.parts[-1]   # Get filename from Pathlib object
    dir = file.parents[0]       # Data directory currently in

    print("Selecting attributes from %s" % filename)

    if not filename.endswith(".arff"):
        print("%s not ARFF file." % filename)
        return

    filename_base = filename[:-5]   # Removes '.arff' from filename
    data = load_Arff_file(file)     # Load data from arff
    data.class_is_first()           # Set first attr as class

    # Define Attribute selection
    search = ASSearch(classname="weka.attributeSelection.Ranker",
                      options=["-T", "0.01", "-N", "-1"])
   # Define Attribute Evaluator
    evaluator = ASEvaluation(
        classname="weka.attributeSelection.CorrelationAttributeEval", options=[])

    # Run attribution selection
    attsel = AttributeSelection()
    attsel.search(search)
    attsel.evaluator(evaluator)
    attsel.select_attributes(data)

    # Define filepath and output results
    attsel_output = filename_base + "_attsel_results.txt"
    output_select_attribute(attsel, dir / attsel_output)

    # Debug Analysis
    print(attsel.selected_attributes)
    for i in range(2):
        Field2.append(attsel.selected_attributes[i])
    for i in range(5):
        Field5.append(attsel.selected_attributes[i])
    for i in range(10):
        Field10.append(attsel.selected_attributes[i])
    for i in range(50):
        Field50.append(attsel.selected_attributes[i])
    print(Field2)
    print(Field5)
    print(Field10)
    print(Field50)

    if len(set(Field10)) == len(Field10):
        print("no duplicates found")

    else:
        print("duplicate found")
        Field50 = list(set(Field50))
        Field10 = list(set(Field10))
        Field5 = list(set(Field5))
        Field2 = list(set(Field2))
    ###


def run_ibk(file):
    # Get filename from Pathlib object
    filename = file.parts[-1]
    dir = file.parents[0]

    print("Running IBk on %s" % filename)

    if not filename.endswith(".arff"):
        print("%s not ARFF file." % filename)
        return

    # Removes '.arff' from filename
    filename_base = filename[:-5]

    # Load data with class as first attr
    data = load_Arff_file(file)
    data.class_is_first()

    # Use IBk and set options
    cls = Classifier(classname="weka.classifiers.lazy.IBk",
                     options=["-K", "3"])
    # print(cls.options)

    # Predictions stored in pout
    pout = PredictionOutput(
        classname="weka.classifiers.evaluation.output.prediction.PlainText")

    # Evaluate data
    evaluation = Evaluation(data)
    evaluation.crossvalidate_model(cls, data, 10, Random(1), output=pout)

    # Save summary, class details and confusion matrix to file
    result_output = filename_base + "_eval_results.txt"
    output_eval(evaluation, dir / result_output)

    # Save the predicited results to file
    prediction_output = filename_base + "_pred_results.txt"
    output_pred(pout, dir / prediction_output)

    print("IBk complete")


def make_dirs():
    for dir in data_dirs:
        data_dirs[dir].mkdir(parents=True, exist_ok=True)


def make_dirs3():
    for dir in data_dirs3:
        data_dirs3[dir].mkdir(parents=True, exist_ok=True)


def make_random_CSVs():
        global Field50
        global Field10
        global Field5
        global Field2

        # Store made arff paths
        arffs = []
        files_created = []

        for file in data_files3:
            if(file.endswith(".csv")):
                if file.startswith("fer2017-training"):
                    print("Reset Globals")
                    files_created = []
                    arffs = []
                    Field50 = []
                    Field10 = []
                    Field5 = []
                    Field2 = []

                files_created += randomise_CSV(file)
                # Convert random csv's to arffs
                for fc in files_created:
                    arff_file = to_ARFF(fc)
                    if arff_file.name.startswith("fer2017-training"):
                        arffs.append(arff_file)

                # Get best attrs of all 3 files
                if file.startswith("fer2017-testing"):
                    # Get best attributes
                    for af in arffs:
                        select_attribute(af)

                    for fc in files_created:
                        make_CSV_SA(fc)



def make_training_set():
    global Field50
    global Field10
    global Field5
    global Field2

    # Store made arff paths
    arffs = []

    for file in data_files3:
        if(file.endswith(".csv")):
            if file.startswith("fer2017-training"):
                print("Reset Globals")
                arffs = []
                Field50 = []
                Field10 = []
                Field5 = []
                Field2 = []

            files_created = splitTestingSets(file)
            # Convert random csv's to arffs
            for fc in files_created:
                arffs.append(to_ARFF(fc))

            # Get best attrs of all 3 files
            if file.startswith("fer2017-testing"):
                # Get best attributes
                for af in arffs:
                    select_attribute(af)

                for fc in files_created:
                    make_CSV_SA(fc)


if __name__ == "__main__":
    init()
