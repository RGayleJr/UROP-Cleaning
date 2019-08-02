
import sys
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import Response
import json
import pandas as pd

sys.path.insert(1, '../')
import DataCleaningFunctions as dcf

# some libs i had to install:
# pip3 install flask 
# pip3 install flask_cors

app = Flask(__name__)
CORS(app)
filename = "../dirtydata/property.csv"
df_orig = pd.read_csv(filename)


# example commands array to send in body of post
# [ "dcf.create_limiting_factor(df, 'PID', 'digits')", "dcf.keep_rows_with_nonenan_within_col(df, 'MOVE_IN_DATE')" ]

@app.route("/cleaned", methods=["POST"])
def customddataset():
    commands = request.get_json()
    print(commands)
    global df_orig
    df = df_orig.copy()

    dcf.initiate(df)
    for c in commands:
        eval(c)

    # reset column headers to just name
    df.columns = [c[0] for c in df.columns]

    return Response(df.to_csv(), mimetype='application/json')

@app.route("/original", methods=["GET"])
def original():
    global df_orig
    return Response(df_orig.to_csv(), mimetype='application/json')

if __name__ == "__main__":
    app.run("0.0.0.0", 9050, threaded=True)