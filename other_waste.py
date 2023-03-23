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

# Define product data as a list of dictionaries
product_data = [
    {"type": "Chair", "length": "2", "height": "1", "width": "3", "status" : "good"},
    {"type": "Table", "length": "12", "height": "12", "width": "32", "status" : "bad"},
    # Add additional products here as needed
]

# Define customer data
name = "Tom"
zip_code = "9000"
street = "Linsebühlstrasse"
number = "101"
date_t = str(date.today())

# Create dictionary for the order
order_dict = {
    "Name": name,
    "Adress": {"Zip": zip_code, "Street": street, "Number": number},
    "Date": date_t,
    "Product": {}
}

# Iterate over the products and add them to the order
for i, product in enumerate(product_data):
    sub_dict = {
        "Product_type": product["type"],
        "Height": product["height"],
        "Width": product["width"],
        "Length": product["length"]
    }
    order_dict["Product"][f"Product_{i}"] = sub_dict

# Create Key Name
key_name = name

# Transform to JSON
json_str = json.dumps(order_dict)
data = json_str.encode('utf-8')

# Upload order data
bucket_name = "starthack"
s3.put_object(Body=data, Bucket=bucket_name, Key=key_name)

# Upload product pictures
for i, product in enumerate(product_data):
    key_name_pic = f"{name}_Product_{i}"
    data_pic = open(f'picture/picture_{i}.png', 'rb')
    s3.put_object(Body=data_pic, Bucket=bucket_name, Key=key_name_pic)

# Download order data
obj = s3.get_object(Bucket=bucket_name, Key=key_name)
json_str = obj['Body'].read().decode('utf-8')
order_dict = json.loads(json_str)

# Download product pictures
for i, product in enumerate(product_data):
    key_name_pic = f"{name}_Product_{i}"
    img_response = s3.get_object(Bucket=bucket_name, Key=key_name_pic)
    picture = img_response['Body'].read()
    img = Image.open(BytesIO(picture))
    img.show()

# Output order data
print(order_dict["Name"])
print(order_dict["Adress"])
print(order_dict["Product"])
print(key_name_pic)
