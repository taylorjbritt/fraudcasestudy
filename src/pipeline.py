import pandas as pd
import numpy as np

def get_avg_ticket_cost(val):
    ticket_costs = []
    for i in range(len(val)):
        ticket_costs.append(val[i]['cost'])
    ticket_quant = []
    for i in range(len(val)):
        ticket_quant.append(val[i]['quantity_total'])
    total = 0
    for cost, quant in zip(ticket_costs, quantities):
        total += cost*quant
    avg = total/sum(quantities)
    return avg

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
    for cost, quant in zip(ticket_costs, quantities):
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



if __name__ == '__main__':

    #read in the dataframe
    df = pd.read_json('../data/data.json')
    #create new fraud column, drop "account type"
    df['fraud'] = df['acct_type'].str[0] == 'f'
    df.drop('acct_type',axis=1,inplace=True)
    def convertunix(columns,df=df):
        '''columns: list of column headers to convert
        df: name of df'''
        for val in columns:
            df[val] = pd.to_datetime(df[val],unit='s')
        return df
    convert = ['approx_payout_date','event_created','event_published','event_start','event_end','user_created']
    convertunix(convert)

    df['tickets_total'] = df['ticket_types'].apply(get_num_tickets)
    df['tiers'] = df['ticket_types'].apply(get_num_tiers)
    df['average_cost'] = df['ticket_types'].apply(get_avg_ticket_cost)
    df['max_cost'] = df['ticket_types'].apply(get_max_ticket_cost)
    df['min_cost'] = df['ticket_types'].apply(get_min_ticket_cost)
    df['total'] = df['ticket_types'].apply(get_total_value)
    df['intl_trans'] = df['country'] != df['venue_country']

    print(df.columns)
