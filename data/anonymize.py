import pandas as pd

raw_data = "raw/FILENAME.csv" #file to be anonymized

savings = pd.read_csv( raw_data )

def anonDict( real_names, name_string ):
    anon_dict = {}
    anon_names = []
    for i in range(len(real_names)):
        anon_names.append( name_string + ' ' + str(i+1) )

    for real, anon in zip(real_names, anon_names):
        anon_dict[real] = anon
    
    return anon_dict

# create anon mappings
contractor_dict = anonDict( savings.contractor.unique(), 'Contractor' )
all_utilities = set(list(savings.electricity_iou.unique()) + list(savings.gas_iou.unique()))
utility_dict = anonDict( list(all_utilities), 'Utility')

# anonymize
savings.contractor = savings.contractor.map(contractor_dict)
savings.electricity_iou = savings.electricity_iou.map(utility_dict)
savings.gas_iou = savings.gas_iou.map(utility_dict)

savings.to_csv( "data/raw/savings.csv", index=False)