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



# Date per Product 1
length = "2"
hight = "1"
width = "3"
poduct = "Chair"

# Date per Product 2
length = "12"
hight = "12"
width = "32"
poduct = "Table"

# Data per Person
name = "Tom"
zip = "9000"
street = "Linsebühlstrasse"
number = "101"
date_t = str(date.today())
count_product = 2


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
key_name = name

# Transforme to Johnson
json_str = json.dumps(my_dict)
data = json_str.encode('utf-8')

# Upload
bucket_name = "starthack"
    # Data
s3.put_object(Body=data, Bucket=bucket_name, Key=key_name)

    # Picture
for i in range(count_product):  
    key_name_pic = my_dict["Name"] + "_Product_" + str(i)
    data_pic = open(f'picture/picture_{i}.png', 'rb')
    s3.put_object(Body=data_pic, Bucket=bucket_name, Key=key_name_pic)


# Download
bucket_name = "starthack"

# Convert back to dictionary
obj = s3.get_object(Bucket=bucket_name, Key=key_name)
json_str = obj['Body'].read().decode('utf-8')
my_dict = json.loads(json_str)

# Download picture
for i in range(count_product):  
    key_name_pic = my_dict["Name"] + "_Product_" + str(i)
    img_response = s3.get_object(Bucket=bucket_name, Key=key_name_pic)
    picture = img_response['Body'].read()
    # Create Image object from data
    img = Image.open(BytesIO(picture))
    # Show Image
    img.show()



# Output Data
print(my_dict["Name"])
print(my_dict["Adress"])
print(my_dict["Product"])
print(key_name_pic)

