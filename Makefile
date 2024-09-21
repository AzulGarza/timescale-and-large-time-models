download_data:
	@mkdir -p data
	@wget https://assets.timescale.com/docs/downloads/get-started/real_time_stock_data.zip -O data/real_time_stock_data.zip 
	@unzip data/real_time_stock_data.zip -d data

populate_timescale: .require-project-id download_data 
	@psql -d ${project_id} -f sql/create_tables.sql

create_materialized_view: .require-project-id
	@psql -d ${project_id} -f sql/create_materialized_view.sql

create_forecasts_table: .require-project-id
	@psql -d ${project_id} -f sql/create_forecasts_table.sql

.require-project-id:
ifndef project_id
	$(error "project_id is not defined")
endif
