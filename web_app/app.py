import pandas as pd
import numpy as np
from datetime import datetime
import re

from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
# import cPickle as pickle
import pickle

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.3.0.79:5000/register"
DATA_SERVER = "http://galvanize-case-study-on-fraud.herokuapp.com/data_point"
DATA = []
TIMESTAMP = []

# Home page with form on it to submit new data
@app.route('/')
def get_new_data():
    return '''
        <form action="/score" method='POST'>
          <br>
          <input type="submit" value="Run fraud prediction on current data">
        </form>
        '''

@app.route('/hello', methods = ['GET'])  
def greet():
    return render_template('hello.html')

@app.route('/score', methods=['POST', 'GET'])
def score():
    new_pt = get_page()
    event_name = new_pt['name'][0]
    new_pt_clean = clean_new_data2(new_pt)
    
    # predict on the new data
    pred = model.predict(new_pt_clean)[0]
    risk = probability(new_pt_clean)
    
    # DATA.append(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
    # TIMESTAMP.append(time.time())
    return render_template('score.html', event=event_name, predicted=pred, risk_level=risk)

def probability(df):
    x = model.predict_proba(df)[0][1]
    if x < .33:
        return 'Low Risk'
    elif x < .66:
        return 'Medium Risk'
    else:
        return 'High Risk'
    

def get_page():
    """Revieves data from the specified url for prediction
    Returns: data (PandasDataFrame): 1 row DataFrame from url"""
    d = json.loads(requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').text)
    data = pd.DataFrame(columns=list(d.keys()))
    data.loc[0] = list(d.values())
    return(data)

def clean_new_data2(df):
    #df=pd.read_json(path_to_file)
    df['tickets_total'] = df['ticket_types'].apply(get_num_tickets)
    df['tiers'] = df['ticket_types'].apply(get_num_tiers)
    df['max_cost'] = df['ticket_types'].apply(get_max_ticket_cost)
    df['min_cost'] = df['ticket_types'].apply(get_min_ticket_cost)
    df['total'] = df['ticket_types'].apply(get_total_value)
    df['intl_trans'] = df['country'] != df['venue_country']
    df['type_one_user'] = df['user_type'] == 1
    df['org_desc_exists'] = [0 if len(df['org_desc'][i])==0 else 1 for i in range(len(df))]
    df['org_name_exists'] = [0 if len(df['org_name'][i])==0 else 1 for i in range(len(df))]
    df['previous_payout_count'] = [len(df.previous_payouts[i]) for i in range(len(df))]
    df['org_facebook'].fillna(value=0, inplace=True)
    df['org_twitter'].fillna(value=0, inplace=True)
    df['org_facebook_exists'] = [0 if df['org_facebook'][i]==0 else 1 for i in range(len(df))]
    df['org_twitter_exists'] = [0 if df['org_twitter'][i]==0 else 1 for i in range(len(df))]
    emaillist = ['ymail.com','lidf.co.uk','live.fr','rocketmail.com','yahoo.fr']
    df.loc[~df["email_domain"].isin(emaillist), "email_domain"] = 0
    df.loc[df["email_domain"].isin(emaillist), "email_domain"] = 1
    countrylist = ['MA','VN','A1','PK','PH','ID','NG','CI','CZ','DZ']
    df.loc[~df["country"].isin(countrylist), "country"] = 0
    df.loc[df["country"].isin(countrylist), "country"] = 1
    df.drop(['object_id', 'name','name_length','num_order','num_payouts','org_facebook','org_twitter','payee_name','payout_type','previous_payouts','previous_payouts','org_name','org_desc','listed','fb_published','event_published','event_end','event_start','event_created','has_logo','has_header','currency','description','approx_payout_date','delivery_method','body_length','channels','gts','sale_duration', 'sale_duration2', 'ticket_types', 'user_created', 'user_type', 'venue_address', 'venue_country', 'venue_latitude', 'venue_longitude', 'venue_name', 'venue_state', 'show_map'],axis=1,inplace=True)
    return df

def get_num_tickets(val):
    ticket_quant = []
    for i in range(len(val)):
        ticket_quant.append(val[i]['quantity_total'])
    return sum(ticket_quant)
def get_num_tiers(val):
    ticket_quant = []
    for i in range(len(val)):
        ticket_quant.append(val[i]['quantity_total'])
    return len(ticket_quant)
def get_total_value(val):
    ticket_costs = []
    for i in range(len(val)):
        ticket_costs.append(val[i]['cost'])
    ticket_quant = []
    for i in range(len(val)):
        ticket_quant.append(val[i]['quantity_total'])
    total = 0
    for cost, quant in zip(ticket_costs, ticket_quant):
        total += cost*quant
    return total
def get_max_ticket_cost(val):
    ticket_costs = []
    for i in range(len(val)):
        ticket_costs.append(val[i]['cost'])
    if len(ticket_costs) == 0:
        return 0
    else:
        return max(ticket_costs)
def get_min_ticket_cost(val):
    ticket_costs = []
    for i in range(len(val)):
        ticket_costs.append(val[i]['cost'])
    if len(ticket_costs) == 0:
        return 0
    else:
        return min(ticket_costs)

# @app.route('/', methods=['GET'])
# def index():
#     """ Render a simple splash page"""
#     return render_template('index.html')

# @app.route('/', methods = ['GET'])  
# def index():
#     return 'Hey there!'



# @app.route('/submit', methods=['GET'])
# def submit():
#     """Render a page containing a textarea input where the user can paste an
#     article to be classified.  """
#     return render_template('submit.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     """Recieve the article to be classified from an input form and use the
#     model to classify.
#     """
#     data = str(request.form['article_body'])
#     pred = str(model.predict([data])[0])
#     return render_template('predict.html', article=data, predicted=pred)

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





@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = DATA[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    model_file = 'web_app/static/rf_taylor_model.pkl'
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    
    # Register for pinging service
    # ip_address = socket.gethostbyname(socket.gethostname())
    # print("attempting to register %s:%d") % (ip_address, PORT)
    # register_for_ping(ip_address, str(PORT))

    # Start Flask app
    # app.run(host='0.0.0.0', port=PORT, debug=True)
    app.run(host='0.0.0.0', port=8082, debug=True)