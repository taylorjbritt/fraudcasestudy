from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
# import cPickle as pickle
import pickle

app = Flask(__name__)
# PORT = 5353
# #REGISTER_URL = "http://10.3.0.79:5000/register"
# #DATA_SERVER = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
# DATA = []
# TIMESTAMP = []

# @app.route('/', methods=['GET'])
# def index():
#     """ Render a simple splash page"""
#     return render_template('index.html')

# @app.route('/hello', methods = ['GET'])  
# def index():
#     return 'Hey there!'

@app.route('/submit', methods=['GET'])
def submit():
    """Render a page containing a textarea input where the user can paste an
    article to be classified.  """
    return render_template('submit.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Recieve the article to be classified from an input form and use the
    model to classify.
    """
    data = str(request.form['article_body'])
    pred = str(model.predict([data])[0])
    return render_template('predict.html', article=data, predicted=pred)

# def get_new_data():
#     """
#     Revieves data from the specified url for prediction
    
#     Returns:
#         data (PandasDataFrame): 1 row DataFrame from url
#     """
#     d = json.loads(requests.get(DATA_SERVER).text)
#     data = pd.DataFrame(columns=list(d.keys()))
#     data.loc[0] = list(d.values())
#     return(data)


# @app.route('/score', methods=['POST'])
# def score():
#     new_pt = get_new_data()
    
#     # predict on the new data
#     Y_pred = model.predict(new_pt)
    
#     DATA.append(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
#     TIMESTAMP.append(time.time())
#     return ""


# @app.route('/check')
# def check():
#     line1 = "Number of data points: {0}".format(len(DATA))
#     if DATA and TIMESTAMP:
#         dt = datetime.fromtimestamp(TIMESTAMP[-1])
#         data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
#         line2 = "Latest datapoint received at: {0}".format(data_time)
#         line3 = DATA[-1]
#         output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
#     else:
#         output = line1
#     return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


# #def register_for_ping(ip, port):
#     registration_data = {'ip': ip, 'port': port}
#     requests.post(REGISTER_URL, data=registration_data)
@app.route('/', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
# the function below will be executed at the host and port followed by '/' 
# the name of the function that will be executed at '/'. Its name is arbitrary.
def index():
    return 'Hello!'

if __name__ == '__main__':
    # model_file = 'static/model.pkl'
    # with open(model_file, 'rb') as f:
    #     model = pickle.load(f)
    
    # Register for pinging service
<<<<<<< HEAD
    #ip_address = socket.gethostbyname(socket.gethostname())
    #print "attempting to register %s:%d" % (ip_address, PORT)
    #register_for_ping(ip_address, str(PORT))
=======
    ip_address = socket.gethostbyname(socket.gethostname())
    print("attempting to register %s:%d") % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))
>>>>>>> e1cc7fac7214d73aaaa7e20495a31061c1a80430

    # Start Flask app
    #app.run(host='0.0.0.0', port=PORT, debug=True)

    app.run(host='0.0.0.0', port=8080, debug=True)