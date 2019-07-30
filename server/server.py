
import sys
from flask import Flask
from flask_cors import CORS
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


# example commands to send are like this
# eval("dcf.create_limiting_factor(df, 'PID', 'digits')")
# eval("dcf.keep_rows_with_nonenan_within_col(df, 'MOVE_IN_DATE')")
@app.route("/cleaned", methods=["POST"])
def customddataset():
    commands = request.get_json()
    print(commands)
    global df_orig
    df = df_orig.copy()

    dcf.initiate(df)
    for c in commands:
        eval(c)

    return Response(df.to_json(), mimetype='application/json')

@app.route("/original", methods=["GET"])
def original():
    global df_orig
    return Response(df_orig.to_json(), mimetype='application/json')

if __name__ == "__main__":
    app.run("0.0.0.0", 9050, threaded=True)


