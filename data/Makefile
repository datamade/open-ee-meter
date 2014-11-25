VPATH=raw:finished:build
include config.mk

GENERATED = summed_savings_kwh_HC.json \
caltrack_merged.csv \
caltest_latlong_clean.csv \
data_prep.txt \
contractor_data_prep.txt


clean:
	@rm -Rf build/*

full_clean:
	@rm -Rf build/*
	@rm -Rf finished/*

all: $(GENERATED)


# clean caltest savings
anon_savings_clean.csv: anon_savings.csv
	@echo "Cleaning savings raw file"
	@csvclean raw/anon_savings.csv
	@mv raw/anon_savings_out.csv build/anon_savings_clean.csv

# clean caltest projects
caltest_projects_clean.csv: caltrack_additional_info.csv
	@echo "Cleaning projects raw file"
	@csvclean raw/caltrack_additional_info.csv
	@mv raw/caltrack_additional_info_out.csv build/caltest_projects_clean.csv

# clean caltest latlong
caltest_latlong_clean.csv: zipcode_to_lat_lng.csv
	@echo "Cleaning zipcode latlong raw file"
	@csvclean raw/zipcode_to_lat_lng.csv
	@mv raw/zipcode_to_lat_lng_out.csv build/caltest_latlong_clean.csv

# merge savings & project info on project id
caltrack_merged.csv: anon_savings_clean.csv caltest_projects_clean.csv
	@echo "Merging savings data & additional project info"
	@python processors/join_csvs.py \
		build/anon_savings_clean.csv \
		build/caltest_projects_clean.csv \
		project_id > build/caltrack_merged.csv

# data processing
data_prep.txt: caltrack_merged.csv
	@python processors/data_prep.py
	@touch finished/data_prep.txt

contractor_data_prep.txt: caltrack_merged.csv
	@python processors/contractor_data_prep.py
	@touch finished/contractor_data_prep.txt

# summary level - elec actual savings (by IOU)
summed_savings_kwh.csv: anon_savings_clean.csv
	@echo "Summing savings (ACTUAL, KWH)"
	@cat build/anon_savings_clean.csv | \
		python processors/sum_by_field.py \
		electricity_iou \
		weather_normalized_yearly_kwh_savings > build/summed_savings_kwh.csv

# summary level - sum elec pred savings (by IOU)
summed_pred_savings_kwh.csv: anon_savings_clean.csv
	@echo "Summing savings (PREDICTED, KWH)"
	@cat build/anon_savings_clean.csv | \
		python processors/sum_by_field.py \
		electricity_iou \
		predicted_yearly_kwh_savings > build/summed_pred_savings_kwh.csv

# summary level - HC elec actual savings (by IUO)
summed_savings_kwh_HC.json: summed_savings_kwh.csv
	@echo "Converting summed savings to JSON highchart input (ACTUAL, KWH)"
	@cat build/summed_savings_kwh.csv | \
		python processors/csv2HCjson.py > finished/summed_savings_kwh_HC.json

# summary level -  HC elec pred savings (by IOU)
summed_pred_savings_kwh_HC.json: summed_pred_savings_kwh.csv
	@echo "Converting summed savings to JSON highchart input (PREDICTED, KWH)"
	@cat build/summed_pred_savings_kwh.csv | \
		python processors/csv2HCjson.py > finished/summed_pred_savings_kwh_HC.json

# summary level -  sum gas actual savings (by IOU)
summed_savings_therm.csv: anon_savings_clean.csv
	@echo "Summing savings (ACTUAL, THERM)"
	@cat build/anon_savings_clean.csv | \
		python processors/sum_by_field.py \
		gas_iou \
		weather_normalized_yearly_therm_savings > build/summed_savings_therm.csv

# summary level -  sum gas pred savings (by IOU)
summed_pred_savings_therm.csv: anon_savings_clean.csv
	@echo "Summing savings (PREDICTED, THERM)"
	@cat build/anon_savings_clean.csv | \
		python processors/sum_by_field.py \
		gas_iou \
		predicted_yearly_therm_savings > build/summed_pred_savings_therm.csv

# summary level -  HC gas pred savings (by IOU)
summed_pred_savings_therm_HC.json: summed_pred_savings_therm.csv
	@echo "Converting summed savings to JSON highchart input (PREDICTED, THERM)"
	@cat build/summed_pred_savings_therm.csv | \
		python processors/csv2HCjson.py > finished/summed_pred_savings_therm_HC.json

# summary level -  HC gas actual savings (by IOU)
summed_savings_therm_HC.json: summed_savings_therm.csv
	@echo "Converting summed savings to JSON highchart input (ACTUAL, THERM)"
	@cat build/summed_savings_therm.csv | \
		python processors/csv2HCjson.py > finished/summed_savings_therm_HC.json

# summary level -  count total and distinct contractors
contractor_counts.json: anon_savings_clean.csv
	@echo "Counting total & distinct contractors"
	@cat build/anon_savings_clean.csv | \
	python processors/count_rows.py \
	contractor > finished/contractor_counts.json

# summary level -  count projects by contractor
projects_by_contractor.csv: anon_savings_clean.csv
	@echo "Counting number of rows (aka projects) by contractor"
	@cat build/anon_savings_clean.csv | \
		python processors/count_distinct_instances.py \
		contractor > build/projects_by_contractor.csv

# summary level - projects by contractor json
projects_by_contractor.json: projects_by_contractor.csv
	@echo "Converting projects by contractor to JSON"
	@cat build/projects_by_contractor.csv | \
		python processors/csv2json.py > finished/projects_by_contractor.json
