from flask import Flask, render_template, request
from static.services.computationservice import *
from static.services.database import *
import json

app = Flask(__name__)

db = Database()


@app.route("/")
def get_front():
    return render_template("index.html")


@app.route("/compute", methods=["POST"])
def compute():
    service = ComputationService(
            np.asarray(json.loads(json.loads(request.get_data(as_text=True))['matrix_a'])),
            np.asarray(json.loads(json.loads(request.get_data(as_text=True))['matrix_b']))
    )
    response, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()

    # Appending all infos to response matrix to facilitate Javascript interpretation
    response = np.append(response, strassen_comp_time * 1000)
    response = np.append(response, strassen_mult_cnt)
    response = np.append(response, classical_comp_time * 1000)
    response = np.append(response, classical_mult_cnt)

    record_stats(int(sqrt(response.size)), strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt)

    return json.dumps(response.tolist())


@app.route('/list-strassen-stats')
def list_strassen_stats():
    return json.dumps(get_stats_rows(db.list_strassen_stats()))


@app.route('/list-classical-stats')
def list_classical_stats():
    return json.dumps(get_stats_rows(db.list_classical_stats()))


@app.route('/reset')
def reset():
    db.reset_table()
    return 'Database reset done.'


def record_stats(matrix_size, s_comp_time, s_mult_cnt, c_comp_time, c_mult_cnt):
    db.add_record(int(matrix_size), float(s_comp_time), int(s_mult_cnt), 1)
    db.add_record(int(matrix_size), float(c_comp_time), int(c_mult_cnt), 0)


def get_stats_rows(rows):
    stats = []
    for row in rows:
        stats.append([str(row[1]), str(row[2]), str(row[3])])
    return stats


if __name__ == '__main__':
    app.run(debug=True)
