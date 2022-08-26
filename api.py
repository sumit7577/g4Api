from crypt import methods
from flask import Flask,json


app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def videoEditor():
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response