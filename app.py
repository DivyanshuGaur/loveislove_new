from flask import Flask,request,jsonify,render_template

from easy_ocr import ocr_image

from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,PorterStemmer
import os
import joblib
import nltk
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.warn("deprecated", DeprecationWarning)

import re



app=Flask(__name__)


CORS(app)




lemmantizer=WordNetLemmatizer()


ext_data=[]
REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
sw=stopwords.words('english')

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
        '''isthisFile.save("test/" + isthisFile.filename)
        data_list=getocr("test/" + isthisFile.filename)'''
        data='Hello world '
        '''for i in data_list:
            data+=i'''
        sentiment=predict(data)
        mp={'data':data,'sentiment':sentiment}
        return jsonify(mp)





def getocr(fn):
    ans = ocr_image(fn, service='youdao')
    print(ans)
    return ans



def predict(data):

    data=data.strip()
    if(data=='' or data==' '):
        return 'Random'

    msg = re.sub('[^a-zA-Z]', ' ', data)
    msg = msg.lower()
    msg = msg.split()
    msg = [lemmantizer.lemmatize(word) for word in msg if not word in sw]
    msg = ' '.join(msg)
    ext_data.append(msg)

    vectors=vectorizer.transform(ext_data)
    pred=classifier.predict(vectors)

    print(pred[0])

    if(pred[0]==0):
        return 'Negative'
    elif(pred[0]==1):
        return 'Positive'






if __name__ == '__main__':
    app.run()