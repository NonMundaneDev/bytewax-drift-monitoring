import pymongo
import pandas as pd
import os
import logging
import boto3


# MongoDB Atlas connection details
mongodb_url = os.environ["mongodb_url"]
collection_name = os.environ["mongodb_collectionname"]

# Connect to MongoDB Atlas
client = pymongo.MongoClient(mongodb_url)
db = client.get_database(collection_name)

def insert_data(pred,issue):
    insert_Data = db[collection_name].insert_one({"pred": pred, "issue": issue})
    try:
        return insert_Data
    except ValueError as ve:
        logging.info(f"Custom error message.{ve} on logging {pred-issue}")
        raise ValueError("Custom error message.") from ve



def retrieve_Data(number_of_row:int):
    cursor = db[collection_name].find().limit(int(number_of_row))
    df = pd.DataFrame(list(cursor))
    # Print the DataFrame
    try:
        return(df)
    except ValueError as ve:
        logging.info(f"Custom error message {ve} on retrieving data")
        raise ValueError("Custom error message on retrieving data") from ve



def data_from_s3(method):
    # Retrieve data from S3 and generate the dashboard
    s3 = boto3.client('s3')
    bucket_name = 'githubissuemlmonitor'
    file_name = 'file.html'
    file_dir = 'app/static/file.html'

    # Download the file from S3
    if method =="get":
        s3.download_file(bucket_name, file_name, file_dir)
    elif method =="post":
        s3.upload_file(file_dir, bucket_name, file_name)


