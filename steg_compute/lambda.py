from steg import *
import os, json, boto3, botocore, base64, pickle

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
        encode_json = s3.Object('steg-compute-data', f'{trans_id}.json')
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
        s3_enc_dump = s3.Object('steg-compute-data', f'encoded/{trans_id}')
        s3_enc_dump.put(Body=enc_nparray_bytes)
        print("Finish np bytes dump into s3")
        
        # Compile dict for response.
        json_response = json.dumps({"function": "encode",
                                   "s3_result_key": f"encoded/{trans_id}"})
        status_code = 200

        print("json response compilation ok")
        
      
      elif req.get("function") == 'decode':
        # Process the content of dict
        enc_img_bytes = bytes(req.get("img_bytes"), encoding='utf8')
        
        # Perform the decoding.
        data, meta = decode_img(read_img_binary(enc_img_bytes))
        
        # Compile dict for response.
        json_response = json.dumps({"function": "decode",
                                   "data_bytes": data.decode("ISO-8859-1"),
                                   "meta": meta})
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
