Open EE Meter
========
Data analysis & visualization of energy savings projects, to ultimately empower utilities and contractors to improve the efficacy of energy savings programs. An open-source project, based upon transparent data standards.

### Project Background

The current state-of-the-art in energy program evaluation is far from ideal, hindered by a lack of feedback loops and misaligned interests. Implementers, utilities, regulators, and contractors are delayed for years without standard and readily accessible calculations of realized savings, restricting their ability to make strategic changes to energy savings programs.

The absence of timely evaluation prevents ongoing comparisons of various programs, implementers, contractors, and utilities, which would otherwise foster healthy competition and benchmarking. These problems exist in spite of increasingly ubiquitous analytics resources, such as interval metering and readily available weather normalization. The Open EE Meter dashboard helps alleviate these problems, by creating a trusted and transparent system to measure and provide near real time feedback on energy savings.

### Dependencies

- [jQuery](http://jquery.com)
- [Highcharts](http://www.highcharts.com/)
- [Bootstrap](http://getbootstrap.com/)

### How to use

#### Adding Data
Put raw data (in csv form) in ```data/raw/```

There should be three raw data files:

1. **savings.csv** - actual & predicted savings for energy savings projects  
     note: if you want to create an anonymized savings.csv file from non-anonymized data, use anonymize.py
     required columns:  
     - project_id
     - contractor
     - electricity_iou
     - gas_iou
     - weather\_normalized\_yearly\_kwh\_savings
     - weather\_normalized\_yearly\_therm\_savings
     - predicted\_yearly\_kwh\_savings
     - predicted\_yearly\_therm\_savings
2. **projects\_additional\_info.csv** - additional info on energy savings projects    
     required columns:  
     - project_id
     - zipcode
     - retrofit\_start\_date
     - retrofit\_end\_date
3. **zipcode\_to\_lat\_lng.csv** - a mapping of zipcodes to their lat/long center    
     required columns:  
     - zipcode
     - lat
     - lng  

#### Processing Data
To prepare and process the data for the open-ee-meter:
```
cd data
make all
```
This will create the ```build/``` & ```finished/``` directories. To clean the ```build/``` & ```finished/``` directories, run ```make full_clean```

#### Running Locally
This is a jekyll site. To run it locally:
```
jekyll serve
```

### Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/open-ee-meter/issues
