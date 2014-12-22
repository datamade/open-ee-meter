VPATH=raw:finished:build
include config.mk

GENERATED = merged.csv \
latlong_clean.csv \
data_prep.txt \
contractor_data_prep.txt


clean:
	@rm -Rf build/*

full_clean:
	@rm -Rf build/*
	@rm -Rf finished/*

all: $(GENERATED)


# clean savings
anon_savings_clean.csv: savings.csv
	@echo "Cleaning savings raw file"
	@csvclean raw/savings.csv
	@mv raw/savings_out.csv build/anon_savings_clean.csv

# clean projects
projects_clean.csv: projects_additional_info.csv
	@echo "Cleaning projects raw file"
	@csvclean raw/projects_additional_info.csv
	@mv raw/projects_additional_info_out.csv build/projects_clean.csv

# clean latlong
latlong_clean.csv: zipcode_to_lat_lng.csv
	@echo "Cleaning zipcode latlong raw file"
	@csvclean raw/zipcode_to_lat_lng.csv
	@mv raw/zipcode_to_lat_lng_out.csv build/latlong_clean.csv

# merge savings & project info on project id
merged.csv: anon_savings_clean.csv projects_clean.csv
	@echo "Merging savings data & additional project info"
	@python processors/join_csvs.py \
		build/anon_savings_clean.csv \
		build/projects_clean.csv \
		project_id > build/merged.csv

# data processing
data_prep.txt: merged.csv
	@python processors/data_prep.py
	@touch finished/data_prep.txt

contractor_data_prep.txt: merged.csv
	@python processors/contractor_data_prep.py
	@touch finished/contractor_data_prep.txt
