import pandas as pd
import numpy as np
from datetime import datetime
import re
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier,AdaBoostRegressor
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
import pickle
import json
import requests

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
    
def clean_df(path_to_file):
    df=pd.read_json(path_to_file)
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
    df.drop(['show_map','object_id', 'name','name_length','num_order','num_payouts','org_facebook','org_twitter','payee_name','payout_type','previous_payouts','previous_payouts','org_name','org_desc','listed','fb_published','event_published','event_end','event_start','event_created','has_logo','has_header','currency','description','approx_payout_date','delivery_method','body_length','channels','gts','sale_duration', 'sale_duration2', 'ticket_types', 'user_created', 'user_type', 'venue_address', 'venue_country', 'venue_latitude', 'venue_longitude', 'venue_name', 'venue_state'],axis=1,inplace=True)
    return df

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

def get_page():
    """Revieves data from the specified url for prediction
    Returns: data (PandasDataFrame): 1 row DataFrame from url"""
    d = json.loads(requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').text)
    data = pd.DataFrame(columns=list(d.keys()))
    data.loc[0] = list(d.values())
    return(data)

def predict_fraud(df, model):
    pred = model.predict(df)
    return pred[0]

if __name__ == '__main__':

    pkl_filename = "../data/rf_taylor_model.pkl"

    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    df_new = get_page()
    df_new = clean_new_data2(df_new)

    print(predict_fraud(df_new, model))

    prediction, event = (predict_fraud(df_new, model)), df_new