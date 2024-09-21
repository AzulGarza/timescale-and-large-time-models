download_data:
	@mkdir -p data
	@wget https://assets.timescale.com/docs/downloads/metrics.csv.gz -O data/metrics.csv.gz
	@gzip -dc metrics.csv.gz > data/metrics.csv

populate_timescale: .require-project-id download_data 
	@psql -d ${project_id} -f sql/create_metrics_table.sql


.require-project-id:
ifndef project_id
	$(error "project_id is not defined")
endif
