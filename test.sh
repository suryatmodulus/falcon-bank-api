#!/bin/bash

TOKEN=""

function getToken(){
	echo $'\n[*] Post Request - For JWT token , URL=https://falcon-bank-api.herokuapp.com/api/getToken?email=modulus@helloworld.in&password=foobar&raw=true'
	response=$(curl -s -XPOST "https://falcon-bank-api.herokuapp.com/api/getToken?email=modulus@helloworld.in&password=foobar&raw=true");
	echo "[*] Server Response : $response"
	TOKEN=$response;
}

function getBankDetailsWithLimitAndOffset(){
	echo $'\n[*] GET Request - For Bank Details with ifsc,limit and offset parameters, URL=https://falcon-bank-api.herokuapp.com/api/getBankDetails?ifsc=BARB0MITHAP&limit=1&offset=0'
 	response=$(curl -s -XGET -H "Authorization: Bearer $TOKEN" "https://falcon-bank-api.herokuapp.com/api/getBankDetails?ifsc=BARB0MITHAP&limit=1&offset=0");
 	echo "[*] Server Response :" 
 	echo "$response"
}


function getBranchDetailsWithLimit(){
	echo $'\n[*] GET Request - For Branch Details with bank_name and limit parameters, URL=https://falcon-bank-api.herokuapp.com/api/getBranchDetails?bank_name=bank+of+baroda&city=chennai&limit=10'
	response=$(curl -s -XGET -H "Authorization: Bearer $TOKEN" "https://falcon-bank-api.herokuapp.com/api/getBranchDetails?bank_name=bank+of+baroda&city=chennai&limit=10");
	echo "[*] Server Response :" 
 	echo "$response"
}

function getBranchDetailsWithLimitAndOffset(){
	echo $'\n[*] GET Request - For Branch Details with bank_name,limit and offset parameters, URL=https://falcon-bank-api.herokuapp.com/api/getBranchDetails?bank_name=bank+of+baroda&city=chennai&limit=5&offset=45'
	response=$(curl -s -XGET -H "Authorization: Bearer $TOKEN" "https://falcon-bank-api.herokuapp.com/api/getBranchDetails?bank_name=bank+of+baroda&city=chennai&limit=5&offset=45");
	echo "[*] Server Response :" 
 	echo "$response"
}

getToken
getBankDetailsWithLimitAndOffset
getBranchDetailsWithLimit
getBranchDetailsWithLimitAndOffset