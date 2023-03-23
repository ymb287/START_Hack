import pandas as pd
import numpy as np
import boto3
from PIL import Image
from io import BytesIO
import json
from datetime import date



# Connect to filesafe
s3 = boto3.client('s3',
	endpoint_url='https://s3.filebase.com',
	aws_access_key_id="53E20FCB7EE046AB8A1C",
	aws_secret_access_key="KJb8C0Nl8HiOl5tu2qHpkPR0zLdpy9mfsWUIAnC2")


# Get the data to safe
img = open('picture/Git_Github.png', 'rb')

# Date per Product
length = "2"
hight = "1"
width = "3"
poduct = "Chair"
count_product = 1

# Data per Person
name = "Tom"
zip = "9000"
street = "Linsebühlstrasse"
number = "101"
date_t = str(date.today())

# Create dictionary for every Entry (multiple Products)
my_dict = {"Name": name, 
           "Adress" : {"Zip": zip, "Street": street, "Numbre": number},
           "Date": date_t,
           "Product" : {}
           }

# Multiple Products
for i in range(count_product):  
    sub_dict = {"Product_type": poduct, "Hight": hight, "Width": width, "Length" : length}
    my_dict["Product"]["Product_" + str(i)] = sub_dict

# Create Key Name
key_name = my_dict["Name"]

# Transforme to Johnson
json_str = json.dumps(my_dict)
data = json_str.encode('utf-8')

# Upload
bucket_name = "starthack"
s3.put_object(Body=data, Bucket=bucket_name, Key=key_name)

# Download
bucket_name = "starthack"

# Convert back to dictionary
obj = s3.get_object(Bucket=bucket_name, Key=key_name)
json_str = obj['Body'].read().decode('utf-8')
my_dict = json.loads(json_str)


# Output Data
print(my_dict["Name"])
print(my_dict["Adress"])
print(my_dict["Product"])


