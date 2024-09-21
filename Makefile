download_data:
	@mkdir -p data
	@wget https://assets.timescale.com/docs/downloads/metrics.csv.gz -O data/metrics.csv.gz
	@gzip -dc metrics.csv.gz > data/metrics.csv
