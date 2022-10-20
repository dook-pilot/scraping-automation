import boto3, os, sys
s3 = boto3.resource(
    service_name='s3',
    region_name='your-region',
    aws_access_key_id='your-access-key',
    aws_secret_access_key='your-secret-key'
)
client = boto3.client('s3', aws_access_key_id='your-access-key', aws_secret_access_key='your-secret-key')

# check if files exist
bovag_datase = os.path.exists('bovag_dataset.csv')
kvk_scrapped_data = os.path.exists('kvk_scrapped_data.csv')
place_api_companies = os.path.exists('place_api_companies.csv')
final_result = os.path.exists('final_result.csv')
if bovag_datase and kvk_scrapped_data and place_api_companies and final_result:
    s3.Bucket('vng-scrapped-data').upload_file(Filename='bovag_dataset.csv', Key='bovag_dataset.csv')
    s3.Bucket('vng-scrapped-data').upload_file(Filename='kvk_scrapped_data.csv', Key='kvk_scrapped_data.csv')
    s3.Bucket('vng-scrapped-data').upload_file(Filename='place_api_companies.csv', Key='place_api_companies.csv')
    s3.Bucket('vng-scrapped-data').upload_file(Filename='final_result.csv', Key='final_result.csv')
    os.remove('bovag_dataset.csv')
    os.remove('kvk_scrapped_data.csv')
    os.remove('place_api_companies.csv')
    os.remove('final_result.csv')
else:
    sys.exit()