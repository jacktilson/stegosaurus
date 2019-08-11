from steg import *
import os, numpy, cv2, bitarray, pathlib, json, boto3, botocore, base64, pickle
from itertools import product, islice
from typing import Iterable, Tuple, Dict, NewType

def lambda_handler(event, context):
    """The function set to be run by AWS Lambda when
    API feeds POSTs and GETs. Designed to be triggered by
    a POST to the api gateway following successful upload
    of JSON to the S3 bucket."""
    print("Lambda begin")
    if event["httpMethod"] == "POST":
      # Unpack POST'd JSON into dict.
      req = json.loads(event["body"])
      
      # Check which function is required.
      if req.get("function") == 'encode':
        print("Encode is the function")
        # Process content of dict.
        trans_id = req.get("trans_id")
        
        # Connect to S3, note no need to auth as lambda in AWS network.
        s3 = boto3.resource('s3')
        
        # Get the JSON containing base64-encoded image and data file bytes from the S3 bucket.
        print("Begin get json from bucket")
        encode_json = s3.Object('steg-compute-data', f'encode/recipe/{trans_id}.json')
        encode_json = encode_json.get()['Body'].read().decode('utf-8') 
        print("Json from bucket done")
        
        # Interpret the JSON.
        encode_recipe = json.loads(encode_json)
        
        # Handle image bytes.
        print("Start process img_bytes")
        img_bytes = encode_recipe.get("img_bytes")
        img_bytes = img_bytes.encode('ascii')
        img_bytes = base64.decodebytes(img_bytes)
        print("Finish process img_bytes")
        
        # Handle data bytes.
        print("Start process data_bytes")
        data_bytes = encode_recipe.get("data_bytes")
        data_bytes = data_bytes.encode('ascii')
        data_bytes = base64.decodebytes(data_bytes)
        print("Finish process data_bytes")

        # Obtain flags, already dict/kwargs type from json.loads()
        flags = encode_recipe.get("flags")
        
        # Perform the encoding.
        print("BEGIN ENCODE CALL")
        encoded_nparray = encode(read_img_binary(img_bytes), data_bytes, **flags)
        print("END ENCODE CALL")
        
        # Convert output to bytes for s3 dump.
        print("Start Serialize nparray")
        enc_nparray_bytes = pickle.dumps(encoded_nparray)
        print("Finish serialize nparray")

        # Dump raw bytes in the S3 bucket.
        print("Start np bytes dump into s3")
        s3_enc_dump = s3.Object('steg-compute-data', f'encode/npbin/{trans_id}')
        s3_enc_dump.put(Body=enc_nparray_bytes)
        print("Finish np bytes dump into s3")
        
        # Compile dict for response.
        json_response = json.dumps({"function": "encode",
                                   "s3_result_key": f"encode/npbin/{trans_id}"})
        status_code = 200

        print("json response compilation ok")
        
      
      elif req.get("function") == 'decode':
        # Process the content of dict
        trans_id = req.get("trans_id")

        # Connect to S3, note no need to auth as lambda in AWS network.
        s3 = boto3.resource('s3')

        # Fetch the recipe containing base64-encoded image bytes from S3.
        print("Begin get json from bucket")
        decode_json = s3.Object('steg-compute-data', f'decode/recipe/{trans_id}.json')
        decode_json = decode_json.get()['Body'].read().decode('utf-8') 
        print("Json from bucket done")

        # Interpret the JSON.
        decode_recipe = json.loads(decode_json)
        
        # Handle image bytes.
        print("Start process enc_img_bytes")
        enc_img_bytes = decode_recipe.get("img_bytes")
        enc_img_bytes = enc_img_bytes.encode('ascii')
        enc_img_bytes = base64.decodebytes(enc_img_bytes)
        print("Finish process enc_img_bytes")
        
        # Perform the decoding.
        data, meta = decode_img(read_img_binary(enc_img_bytes))

        # Prepare the resultant bytes for HTTP.
        data_bytes = base64.encodebytes(data)
        data_bytes = data_bytes.decode('ascii')

        # Fetch metadata
        filename = meta.get("filename", "output") #defaults to "output" if "filename" not present 
        extension = meta.get("extension", "") #defaults to "" if "extension" not present
        out_filename = f"{filename}.{extension}" if extension != "" else filename

        # Compile JSON for dump in S3.
        decode_json = json.dumps({"function": "decode",
                                  "data_bytes": data_bytes,
                                  "file_name": out_filename})

        # Dump raw bytes in the S3 bucket.
        print("Start json bytes dump into s3")
        s3_dec_dump = s3.Object('steg-compute-data', f'decode/decbin/{trans_id}.json')
        s3_dec_dump.put(Body=decode_json)
        print("Finish json bytes dump into s3")
        

        # Compile dict for response.
        json_response = json.dumps({"function": "decode",
                                  "s3_result_key": f"decode/decbin/{trans_id}.json"})
        
        status_code = 200
        
      else:
        json_response = json.dumps({"function": "undefined",
                                    "error": "API doesn't know how to handle this POST."})
        status_code = 400
   
    else:
      json_response = json.dumps({"function": "undefined",
                                  "error": "API only handles POST requests."})
      status_code = 400
        
    # Reply to request.
    return {
        'statusCode': status_code,
        'headers': { "header": "application/json" },
        'body': json_response
    }
