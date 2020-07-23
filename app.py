from flask import Flask,request,jsonify,render_template

from easy_ocr import ocr_image

from flask_cors import CORS

import os
import joblib
import nltk
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.warn("deprecated", DeprecationWarning)

import re



app=Flask(__name__)


CORS(app)




data_list=[]

ext_data=[]
REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

'''classifier=joblib.load('Models/LogReg.pickle')
vectorizer=joblib.load('Models/Vectorizer.pickle')
'''

@app.route("/")
def index():
    return render_template('homepage.html')




@app.route('/analyse/', methods=['GET', 'POST'])
def analayse():
    if (request.method == 'POST'):
        isthisFile = request.files.get('file')
        print(isthisFile.filename)
        isthisFile.save("./" + isthisFile.filename)
        data_list=getocr(isthisFile.filename)
        data=''
        for i in data_list:
            data+=i
        mp={'data':data,'sentiment':'positive'}
        return jsonify(mp)


def getocr(fn):
    ans = ocr_image(fn, service='youdao')
    print(ans)
    return ans









if __name__ == '__main__':
    app.run()
