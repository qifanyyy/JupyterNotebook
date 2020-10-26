import csv
import time

def get_filename():
    """Returns a filename with a timestamp in it to ensure unique filenames"""
    timestr = time.strftime("%Y-%m-%d--%H-%M-%S")
    return f"benchmark_data/benchmark-{timestr}"

def average(arr):
    """Takes an array of numbers and returns the average."""
    arrSum = 0
    count = 0
    try:
        for i in arr:
            if i > -1:
                arrSum += i
                count += 1
        return (arrSum / count)
    except:
        return -1

def transform_data(data_dict: dict):
    """
    Takes the original data dict and converts it to a dict containing the fieldnames
    and an array of dict in a form that can be used by csv.DictWriter 
    (each element of array representing a CSV row), e.g.
    {fieldnames: ["input_len", "trial1", ...], results: [{'input': 15, 'trial1': 4738, 'trial2': 4367, ..., 'average': 47248}]}
    """
    field_names = ["input_len"]
    for i in range(1, len(data_dict[list(data_dict.keys())[0]]) + 5): # length of array of first value
        field_names.append(f"trial{i}")
    field_names.append("average")
    results = []
    for i in data_dict.keys():
        theDict = {"input_len": len(str(i)), "average": average(data_dict[i])}
        trialNum = 1
        for j in data_dict[i]:
            theDict[f"trial{trialNum}"] = j
            trialNum += 1
        results.append(theDict)
    return {"fieldnames": field_names, "results": results}

def write_data(data_dict: dict, filename=None):
    """
    Takes a dictionary of data of the form {inputNum: [result1, result2, ...]}
    and outputs the data as a CSV for the form:
    input, trial1, trial2, trial3, ..., average
    """
    data = transform_data(data_dict)
    if filename is None:
        filename = get_filename()
    with open(filename, 'w') as csvfile:
        fieldnames = data["fieldnames"]
        rows = data["results"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return filename

def test():
    print("Running CsvDataWriter test...")
    test_dict = {
        1: [1, 2, 3, 4],
        5: [123, 423, 532, 748],
        15: [647, 616, 679, 686]
    }
    filename = get_filename()
    write_data(test_dict, filename=filename)
    return filename

if __name__ == "__main__":
    test()