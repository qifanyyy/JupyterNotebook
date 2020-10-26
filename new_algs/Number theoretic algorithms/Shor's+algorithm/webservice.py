from flask import Flask, render_template, request, url_for
from shor import main
import json

app = Flask(__name__, template_folder="templates")

@app.route("/")
def homepage():
    #return "hello world"
    return render_template('index.html')

@app.route("/calculate", methods=["POST"])
def calculate():
    if request.method == "POST":
        factors_array = []
        print("CALCULATE FACTORS")
        data = request.get_json(force=True)
        print("N: ", data['inputN'])
        user_input = int(data['inputN'])
        #factors_array = main(user_input)
        print("FACTORS:")
        if(user_input < 0):
            user_input = user_input * -1
        f1, f2 = main(user_input)
        print(f1, f2)
        return json.dumps({"f1":f1, "f2":f2})
    return json.dumps({"f1":0, "f2":0})

if __name__ == "__main__":
    app.run(port=5001, debug=True)