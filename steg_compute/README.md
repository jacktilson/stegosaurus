# steg_compute
The code called by steg-compute lambda function in AWS for encode and decode operations. 
Note that a valid AWS access key and secret key are required in order to access the S3 bucket used in transactions.
The lambda function is triggerable by making calls to the associate API route which is able to handle POST requests.

To deploy, the structure of the zip must be:

[`bitarray`]
[`cv2`]
[`numpy`]
[`cryptography`]
[`steg.py`]
[`lambda.py`]

Note that [`steg.py`] is the core code for the stegosaurus encode and decode, and its dependent functions.
You should use [`pip install bitarray cv2 numpy cryptography -t .`] to obtain the dependencies listed above.
