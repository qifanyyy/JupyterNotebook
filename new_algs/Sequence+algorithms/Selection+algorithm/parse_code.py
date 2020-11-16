import argparse
import os
import time

from tasks.data import dataset_tasks as dt


def parse_c_code(file_path, out_path):

    if 'PESCO_PATH' not in os.environ:
        raise ValueError(
                    "Environment variable PESCO_PATH has to be defined!")
    if not os.path.isfile(file_path):
        raise ValueError("Some problem occur while accessing file %s." % file_path)

    pesco_path = os.environ['PESCO_PATH']
    out_pos = out_path+".pos"

    start_time = time.time()

    print("Run PeSCo graph generation on %s" % file_path)
    dt.run_pesco(
        pesco_path,
        file_path,
        out_path,
        pos_path=out_pos
    )

    run_time = time.time() - start_time

    if not os.path.exists(out_path):
        raise ValueError(
            "Pesco doesn't seem to be correctly configured! No output for %s" % file_path
        )

    return out_path, out_pos, run_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("out_path")

    args = parser.parse_args()

    fp = os.path.abspath(args.file_path)
    op = os.path.abspath(args.out_path)

    print("Start parsing: %s" % args.file_path)

    try:
        parse_c_code(fp, op)
    except ValueError as e:
        print(e)
        print("If PeSCo is not installed, install the tool by setup-pesco.sh bash script.")
