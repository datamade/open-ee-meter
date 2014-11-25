import pandas as pd
from pandas import to_datetime
import numpy
import json
import re
import os

projects = pd.read_csv( "build/caltrack_merged.csv")
loc = pd.read_csv( "build/caltest_latlong_clean.csv")

merged = projects.merge(loc, on="zipcode")

contractor_dict = {
    'electricity_iou': {
        'contractor_names' : ['Contractor 12'],
        'actual_col' : 'weather_normalized_yearly_kwh_savings',
        'pred_col': 'predicted_yearly_kwh_savings',
        'hist_chunks' : [float(i)/2 for i in range(-8, 9)]
        }, 
    'gas_iou': {
        'contractor_names' : ['Contractor 12'],
        'actual_col' : 'weather_normalized_yearly_therm_savings',
        'pred_col': 'predicted_yearly_therm_savings',
        'hist_chunks' : [float(i)/4 for i in range(-8, 9)]
        }
    }


def getBuckets(freq, cutoffs):
    buckets = []
    for i in range(len(freq)):
        bucket = str(cutoffs[i])+' to '+str(cutoffs[i+1])
        buckets.append(bucket)
    return buckets

def monthLabel(date_string):
    year = date_string[:4]
    month_num = date_string[5:7]
    months = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    month = months[month_num]
    label = month + ' ' + year
    return label

def quarterLabel(date_string):
    year = date_string[:4]
    month_num = date_string[5:7]
    quarters = {
        '03': 'Q1',
        '06': 'Q2',
        '09': 'Q3',
        '12': 'Q4'
    }
    qtr = quarters[month_num]
    label = qtr + ' ' + year
    return label


for utility_type in contractor_dict:
    if not os.path.exists('finished/contractor/'+utility_type):
        os.makedirs('finished/contractor/'+utility_type)

    print "Processing", utility_type
    contractor_names = contractor_dict[utility_type]["contractor_names"]
    actual_col = contractor_dict[utility_type]["actual_col"]
    pred_col = contractor_dict[utility_type]["pred_col"]

    all_projects = merged[['project_id', 'contractor', utility_type, actual_col, pred_col, 'retrofit_end_date']]
    all_projects['realization_rate'] = all_projects[actual_col]/all_projects[pred_col]
    projects_rr = all_projects[ numpy.isnan(all_projects['realization_rate']) == False]
    projects_rr = projects_rr[ projects_rr[actual_col] != 0 ]
    projects_rr = projects_rr[ projects_rr[pred_col] != 0 ]
    projects_rr['date'] = to_datetime(projects_rr['retrofit_end_date'])

    for contractor_name in contractor_names:
        print contractor_name
        slug = re.sub('[\W]+', '_', contractor_name)

        # all projects
        utility_data_all = all_projects[all_projects["contractor"] == contractor_name]
        # only projects w/ valid rr
        utility_data_clean = projects_rr[ projects_rr["contractor"] == contractor_name ]

        ###########################################
        # prep realization rate distribution ######
        ###########################################
        utility_rr_vals = utility_data_clean['realization_rate']
        utility_rr_vals = list(numpy.round(utility_rr_vals, 2))
        utility_rr_vals.sort()
        hist_chunks = contractor_dict[utility_type]["hist_chunks"]
        freq, cutoffs = numpy.histogram(utility_rr_vals, hist_chunks)
        freq = list(freq)
        buckets = getBuckets(freq, cutoffs)

        utility_json = {}
        utility_json["name"] = contractor_name
        utility_json["slug"] = slug

        utility_json["rr_histogram"] = {}
        utility_json["rr_histogram"]["xlabels"] = buckets
        utility_json["rr_histogram"]["dataseries"] = {}
        utility_json["rr_histogram"]["dataseries"]["data"] = freq
        utility_json["rr_histogram"]["dataseries"]["name"] = "projects"

        ###########################################
        # prep counts #############################
        ###########################################

        utility_json["counts"] = {}
        utility_json["counts"]["total_projects"] = len(utility_data_all)
        utility_json["counts"]["total_projects_rr"] = len(utility_data_clean)
        utility_json["counts"]["total_contractors"] = len(utility_data_all['contractor'].unique())


        ###########################################
        # prep realization rate time series #######
        ###########################################

        monthly_rr = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('M', how='mean')

        utility_json['rr_timeseries'] = {}
        utility_json['rr_timeseries']["xlabels"] = []
        utility_json['rr_timeseries']["rr"] = []
        utility_json['rr_timeseries']["errors"] = []
        """
        if len(monthly_rr) == len(monthly_rr.dropna()):
            stdev = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('M', how='std')
            count = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('M', how='count')
            monthly_rr['stderr'] = stdev/numpy.sqrt(count['realization_rate'])
            monthly_rr['confint_lo'] = monthly_rr['realization_rate'] - monthly_rr['stderr']
            monthly_rr['confint_hi'] = monthly_rr['realization_rate'] + monthly_rr['stderr']

            for row in monthly_rr.iterrows():
                utility_json['rr_timeseries']['xlabels'].append( monthLabel(str(row[0])) )
                utility_json['rr_timeseries']['rr'].append(row[1]['realization_rate'])
                utility_json['rr_timeseries']['errors'].append( [ row[1]['confint_lo'], row[1]['confint_hi'] ] )
        else:
        """
        quarterly_rr = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('Q', how='mean')
        stdev = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('Q', how='std')
        count = utility_data_clean[['date', 'realization_rate']].set_index('date').resample('Q', how='count')
        quarterly_rr['stderr'] = stdev/numpy.sqrt(count['realization_rate'])
        quarterly_rr['confint_lo'] = quarterly_rr['realization_rate'] - quarterly_rr['stderr']
        quarterly_rr['confint_hi'] = quarterly_rr['realization_rate'] + quarterly_rr['stderr']
        quarterly_rr_clean = quarterly_rr.dropna()

        for row in quarterly_rr_clean.iterrows():
            utility_json['rr_timeseries']['xlabels'].append( quarterLabel(str(row[0])) )
            utility_json['rr_timeseries']['rr'].append(row[1]['realization_rate'])
            utility_json['rr_timeseries']['errors'].append( [ row[1]['confint_lo'], row[1]['confint_hi'] ] )

        ###########################################
        # prep savings sums #######################
        ###########################################
        utility_json['savings_sums'] = {}
        sum_actual = utility_data_all[actual_col].sum()
        sum_pred = utility_data_all[pred_col].sum()
        utility_json['savings_sums']['actual']= int(sum_actual)
        utility_json['savings_sums']['pred']= int(sum_pred)

        ###########################################
        # prep savings by contractor ##############
        ###########################################
        utility_json['savings_by_contractor'] = {}
        utility_json['savings_by_contractor']['series_pred'] = {}
        utility_json['savings_by_contractor']['series_pred']['name'] = "Predicted Yearly Savings"
        utility_json['savings_by_contractor']['series_pred']['data'] = []
        utility_json['savings_by_contractor']['series_actual'] = {}
        utility_json['savings_by_contractor']['series_actual']['name'] = 'Yearly Savings (Weather Normalized)'
        utility_json['savings_by_contractor']['series_actual']['data'] = []
        utility_json['savings_by_contractor']['xlabels'] = []
        utility_json['savings_by_contractor']['series_counts'] = []

        df = utility_data_all[['contractor', actual_col, pred_col]]
        
        grouped = df.groupby('contractor')

        for contractor, data in grouped:
            # only include contractors w/ number of projects over threshold. smarter way of setting threshold?
            threshold = 10
            num_projects = data[pred_col].count()
            if num_projects > threshold:
                sum_pred = data[pred_col].sum()
                sum_actual = data[actual_col].sum()

                avg_pred = sum_pred/num_projects
                avg_actual = sum_actual/num_projects


                """
                # what to do if nan?
                if numpy.isnan(data[pred_col].sum()):
                    sum_pred = 0
                if numpy.isnan(data[actual_col].sum()):
                    sum_actual = 0
                """
                utility_json['savings_by_contractor']['series_pred']['data'].append( int(avg_pred) )
                utility_json['savings_by_contractor']['series_actual']['data'].append( int(avg_actual) )
                utility_json['savings_by_contractor']['xlabels'].append( contractor )
                utility_json['savings_by_contractor']['series_counts'].append( num_projects )
            else:
                i = i
            

        filename = 'finished/contractor/'+utility_type+'/'+slug+'.json'
        with open(filename, 'w+') as f:
            f.write(json.dumps(utility_json, indent=4))


contractor_summary_names = ['Contractor 12']
if not os.path.exists('finished/contractor/summary'):
    os.makedirs('finished/contractor/summary')

for contractor_name in contractor_summary_names:
    slug = re.sub('[\W]+', '_', contractor_name)
    utility_projects = merged[ merged["contractor"] == contractor_name ]
    utility_projects = utility_projects[ utility_projects["contractor"] == contractor_name ]

    utility_json = {}
    utility_json["name"] = contractor_name
    utility_json["slug"] = slug
    utility_json["latlong"] = []
    utility_json["total_projects"] = len(utility_projects)
    utility_json["total_contractors"] = len(utility_projects.groupby('contractor'))

    for row in utility_projects.iterrows():
        lat = row[1]["lat"]
        lng = row[1]["lng"]
        utility_json['latlong'].append([lat, lng])

    filename = 'finished/contractor/summary/'+slug+'.json'
    with open(filename, 'w+') as f:
        f.write(json.dumps(utility_json, indent=4))


    


