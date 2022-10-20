# Introduction
This project contains the scripts for scraping the web data and storing it into csv file, then upload the csv file on s3 bucket and also the csv data into the PostgreSQL database.
# Installation
First create a virtual environment using virtualenv program. Activate the virtual environment.
pip install -r requirements.txt --default-timeout=100
# Usage:
# scraping files
"bvg_web_scrapper.py" file is responsible for scraping data from [bovag](https://www.bovag.nl/zoek-bovag-bedrijf?l=The%20hague&d=-1&s=distance#search) website. It stores the scrapped data into bovag_dataset.csv file.
"kvk_scrapper.py" file is responsible for scraping data from [kvk](https://www.kvk.nl/zoeken/) website. It stores the scrapped data into kvk_scrapped_data.csv file.
"VNG_company_name_matching.py" is responsible for comparing 2 files (bovag_dataset.csv and place_api_companies.csv). It extracts similarities and gives output as a dataframe "df2".
# DB Files
"bovag_db.py" is responsible for storing bovag_dataset.csv data into PostgreSQL database inside the bovag table.
"kvk_db.py" is responsible for storing kvk_scrapped_data.csv data into PostgreSQL database inside the kvk table.
"place_api_companies.py" is responsible for storing place_api_companies.csv data into PostgreSQL database inside the place_api_companies table.
"companies_irregularities_db.py" is responsible for storing final_result.csv data into PostgreSQL database inside the companies_irregularities table.
# Backup
We are using AWS S3 Bucket to store csv files as a backup there. Right after the new scrapped data, csv files will be updated and uploaded to s3 bucket.
"update_s3_bucket.py" is responsible for doing this task.
