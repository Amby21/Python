# import packages
import os
import requests
import awswrangler as wr
import boto3
import pandas as pd
from dotenv import load_dotenv
import urllib
import json
import time
from datetime import datetime
from tqdm import tqdm
import asyncio
from requests.adapters import HTTPAdapter, Retry

# 1. Extract properties file from AWS bucket
# %% Reading data from s3 bucket
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
api_key_cherre = os.getenv('api_key_cherre')
api_url_cherre = os.getenv('api_url_cherre')
s3_bucket = 'bucket'
s3_location = 'filename'
address = ""
lat = 0.0
long = 0.0



# Reading csv from the aws path
# path = f"s3://{s3_bucket}/{s3_location}"
# raw_df = wr.s3.read_csv(path)
raw_df = pd.read_csv('C:/Users/sganesh/Downloads/property_list_02092023_short.csv')
# print(raw_df)
# API URL from Bing Maps
api_url_bing = f'http://dev.virtualearth.net/REST/v1/Locations?'
api_key_bing = os.getenv('api_key')


# Function declaration to get geopoints for the locations in excel file
def getGeoPoints(data_row):
    value = data_row[
        ['City', 'Postal Code', 'Country', 'Street Address', 'State/Province/District']].isnull().values.any()
    if value:
        return data_row['ID'], 0.0, 0.0
    else:
        print(value)
        try:
            # Integration with the BingMaps API
            locality = data_row['City']
            postalCode = data_row['Postal Code']
            countryRegion = data_row['Country']
            addressLine = data_row['Street Address']
            adminDistrict = data_row['State/Province/District']

            # Parameters to be passed into the base URL
            parameters = {"countryRegion": countryRegion,
                          "adminDistrict": adminDistrict,
                          "locality": locality,
                          "postalCode": postalCode,
                          "addressLine": addressLine,
                          "key": api_key_bing}
            # API URL with variables embedded
            response = requests.get(f"{api_url_bing}{urllib.parse.urlencode(parameters)}")
            api_data = json.loads(response.content)

            # Storing Coordinates from the API response
            geoPoints = api_data.get("resourceSets")[0].get("resources")[0].get("point").get("coordinates")
            # print(api_data)
            return data_row['ID'], (geoPoints[0]), (geoPoints[1])
        except:
            # print(response.text)
            return data_row['ID'], 0.0, 0.0


status_code = 200
# DEFINING FUNCTION FOR GETTING RECORDS
# %% headers for cherre api
apiHeaders = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key_cherre}


def get_response(data_row, url, query, statusCode, headers, variables):
    while True:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code == statusCode:
            try:
                cherre_id = response.json()["data"]["tax_assessor_point"][0]['cherre_parcel_id']
                return cherre_id
            except:
                return 'None'
        elif response.status_code == 503 or response.status_code == 504:
            time.sleep(5)  # pause execution for 5 seconds before retrying
            continue
        else:
            print(response.text)
            raise Exception(f"Unexpected status code returned: {response.status_code}")


x = []
result = []
cherre_parcel_id = list()


# Looping through all rows for function call to get coordinates
# for index, row in tqdm(raw_df.iterrows())
def process_row(row):
    response = list(getGeoPoints(row))
    print(response[1])
    print(response[2])
    if row['Country'] == 'US':
        print(response[1])
        print(response[2])
        query1 = '''query Myquery ($latitude: float8!, $longitude: float8!) {
          tax_assessor_point(args: { latitude: $latitude, longitude: $longitude }) {
            cherre_parcel_id }} '''
        variables = {
            "latitude": response[1],
            "longitude": response[2]
            }
        cherre_parcel_id = get_response(row, api_url_cherre, query1, status_code, apiHeaders, variables)
        if cherre_parcel_id:
            response.append(cherre_parcel_id)
            result.append(response)
        else:
            response.append('None')
            result.append(response)
    else:
       response.append('None')
       result.append(response)



# loop through all the rows, using the apply function.
raw_df.apply(process_row, axis=1)
# print(result)
# %% Creating a dataframe from the list of coordinates and cherre parcel id.
df_geoPoints_cherre = pd.DataFrame(result, columns=['ID', 'Latitude', 'Longitude']) #, 'Cherre_id'
print(df_geoPoints_cherre.head(10))
# Merge geopoints and cherre parcel id dataframe to the main dataframe
final_df = pd.merge(raw_df, df_geoPoints_cherre, on=['ID'], how='inner')
#
# # Write the dataframe to a CSV file
variable = "property_geocode_cherre"
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename = variable + current_date + '.csv'
final_df.to_csv(filename, index = False)

# Upload the CSV file to S3
s3_client = boto3.client('s3')
variable = "property_geocode_cherre"
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filename = variable + current_date + '.csv'
s3_client.upload_file(filename, 'property-list-silver',filename)

# Push data from AWS Glue to Redshift
conn = psycopg2.connect(dbname ='brookfield-properties',
                                      host = host,
                                      port = '1234',
                                      user = user,
                                      password = passwrd
                                      )

tablename = 'brookfield_properties_geo_cherre'
to_path=f"s3://{s3_bucket}/{s3_location}"
# print(from_path)
querry = "COPY {} FROM '{}' CREDENTIALS 'aws_access_key_id={};aws_secret_access_key={};[;token={}]' IGNOREHEADER 1 CSV;".format(tablename,to_path,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN)