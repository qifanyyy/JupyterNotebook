from flask import Flask, render_template, request, flash, redirect, url_for
import os
from pathlib import Path
import algorithm as alg

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.secret_key = 'super secret key'


@app.route('/')
def open_discription():
    return render_template('algorithm.html')


@app.route('/generation')
def open_generation():
    return render_template('generation.html')


@app.route('/generation', methods=['POST'])
def my_form_post():
    result = request.form
    pydict = result.to_dict(flat=False)
    if (pydict.get('size')[0] != '' and pydict.get('from')[0] != '' and pydict.get('to')[0] != ''):
        size = int(pydict.get('size')[0])
        a = int(pydict.get('from')[0])
        b = int(pydict.get('to')[0])
    else:
        flash("Заполните все поля!")
        return redirect(url_for('open_generation'))
    print(size)
    if size < 6 or size > 18:
        flash("Количество вершин должно быть от 6 до 18!")
        return redirect(url_for('open_generation'))
    if a > b:
        flash("Ошибка ввода границ весов ребер!")
        return redirect(url_for('open_generation'))
    alg.runAlg(size, a, b)
    return render_template('graph.html')


@app.route('/circle')
def load():
    images = []
    i = 1
    while os.path.isfile('static/pics/step' + str(i) + '.svg'):
        images.append('static/pics/step' + str(i) + '.svg')
        i += 1
    print(images)
    return render_template("circle.html", images=images)


@app.route('/rect')
def load_rect():
    images = []
    i = 1
    while os.path.isfile('static/pics/step' + str(i) + '_rect.svg'):
        images.append('static/pics/step' + str(i) + '_rect.svg')
        i += 1
    print(images)
    return render_template("rect.html", images=images)


@app.route('/graph')
def run():
    return render_template('graph.html')


@app.route('/graph')
def error():
    if not os.path.isfile('static/pics/graphRect_final.svg'):
        flash('НОД для данного графа отсутсвует')
        return render_template('graph.html')


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
    app.templates_auto_reload = True
