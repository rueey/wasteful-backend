import subprocess
import numpy
import json
import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from PIL import Image
import sys

# by Rui

UPLOAD_FOLDER = 'Queries/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        if(file and allowed_file(file.filename)):
            filename = secure_filename("query."+file.filename.rsplit('.', 1)[1].lower())
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return get_predictions(filename)
    except:
        print(sys.exc_info()[1])
    
    return "Error"

def get_predictions(filename):
    s = subprocess.check_output(["python", "label_image.py", "--graph=output_graph.pb", "--labels=output_labels.txt", "--input_layer=Placeholder", "--output_layer=final_result", "--image=Queries/"+filename])
    s = s.decode("utf8").replace("'", '"')
    s = "{\n"+s+"}"

    result = ""
    for x in range(0, len(s)):
        if(s[x] == ' ' and s[x+1].isdigit()):
            result += "\": "
        elif(s[x] == '\n' and s[x-1] != "{" and s[x+1] != "}"):
            result += ",\n\""
        elif(s[x] == '\n' and s[x+1] != "}"):
            result += "\n\""
        else:
            result += s[x]

    data = json.loads(result)
    result = json.dumps(data, indent=4)

    return result