VPATH=raw:finished:build
include config.mk

GENERATED = caltrack_merged.csv \
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
