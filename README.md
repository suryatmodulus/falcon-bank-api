# Falcon-Bank-API

A Restful API powered by Falcon, JWT Auth and Postgresql DB


### To Test the API :
	
	sudo chmod+x test.sh
	./test.sh
  

# POST ROUTES

### For JWT Token : 

Request parameters :

| parameter | Required | Description |
| --------- | -------- | -----------
| 	email   |    Yes   | User Email  |
|  password |    Yes   | User Password,|
|   raw     | Optional | when set to "true" return plain Token text, default format is JSON| 

To test the API use email=modulus@helloworld.in and password=foobar (You change this in api.py)

Example : 

	echo $(curl -s -XPOST "https://falcon-bank-api.herokuapp.com/api/getToken?email={email}&password={raw}&raw=true");

# GET ROUTES

### For Bank Details : 

Request URL : https://falcon-bank-api.herokuapp.com/api/getBankDetails
	
Request parameters :

| parameter | Required | Description |
| --------- | -------- | ----------- |
|    ifsc   |    Yes   |  IFSC Code  |
|   limit   | Optional |  limit data |
|   offset  | Optional | offset data |

token = JWT token from the post request

Example : 

   TOKEN={token} && echo $(curl -s -XGET -H "Authorization: Bearer $TOKEN" "https://falcon-bank-api.herokuapp.com/api/getBankDetails?ifsc={ifsc}&limit={limit}&offset={offset}");
    


### For Branch Details : 

Request URL : https://falcon-bank-api.herokuapp.com/api/getBranchDetails
	
Request parameters :

| parameter | Required | 
| --------- | -------- |
| bank_name |    Yes   |
|    city   |    Yes   |
|   limit   | Optional |
|   offset  | Optional |   

token = JWT token from the post request

Example : 

   TOKEN={token} && echo $(curl -s -XGET -H "Authorization: Bearer $TOKEN" "https://falcon-bank-api.herokuapp.com/api/getBranchDetails?bank_name={bank_name}&city={city}&limit={limit}&offset={offset}");
    

# Data Dump :
	
	https://github.com/snarayanank2/indian_banks