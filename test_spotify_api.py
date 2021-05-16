import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator
import csv
import random
import pprint
from requests.models import Response
import base64
from creds import *

# This method returns a bearer token for the clientId and Client Secret specified in creds.py 
def get_access_token():
     """
        Returns Bearer Token
     """
     url = 'https://accounts.spotify.com/api/token'
     headers = {}
     data = {}
     # Encode as Base64
     encodedMessage = f"{clientId}:{clientSecret}"
     messageBytes = encodedMessage.encode('ascii')
     base64Bytes = base64.b64encode(messageBytes)
     base64Message = base64Bytes.decode('ascii')
     # Now include the headers for token api and get the access token
     headers['Authorization'] = f"Basic {base64Message}"
     data['grant_type'] = "client_credentials"
     resp = requests.post(url, headers=headers, data=data)
     token = resp.json()['access_token']
     return token

bearerToken = 'Bearer '+ get_access_token()

                                              # Test Cases for Fetch artistId API

# This method tests the search api for the type artist and returns artist Id
def  test_fetch_artist_id():
     url = 'https://api.spotify.com/v1/search'
     artistName = 'A.R. Rahman'
     queryParams = {'query': artistName, 'offset': '0','limit': '20','type':'artist'}
     headers = {"Authorization": bearerToken}
     response = requests.get(url,headers=headers,params=queryParams)
     assert response.status_code == 200
     resp = json.loads(response.text)
     # Fetch artist Id matching with artist name from the items array 
     print('Number of Artists :',resp['artists']['items'].__len__())
     for row in resp['artists']['items']:
          if row['name'] == artistName:
                artistId=row['id']
                print('Matched Artist id :',artistId)  
       
     return artistId

# This method verifies the 401 code by ignoring the token in url for fetch artist Id API
def test_fetch_artist_id_no_token_401():
     url = 'https://api.spotify.com/v1/search'
     artistName = 'A.R. Rahman'
     queryParams = {'query': artistName, 'offset': '0','limit': '20','type':'artist'}
     response = requests.get(url,params=queryParams)
     resp = json.loads(response.text)
     print('Fetch Artist Id, no token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'No token provided'

# This method verifies the invalid id case for fetch artist Id API
def est_fetch_artist_id_400():
     url = 'https://api.spotify.com/v1/search'
     artistName = 'nssfsinf'
     queryParams = {'query': artistName, 'offset': '0','limit': '20','type':'artist'}
     headers = {"Authorization": bearerToken}
     response = requests.get(url,headers=headers,params=queryParams)
     assert response.status_code == 400
     resp = json.loads(response.text)
     print('Fetch Artist Id, invalid id error response:',resp)  
     assert resp['error']['status'] == 400
     assert resp['error']['message'] == 'invalid id'

# This method verifies the 401 code by passing expired token in url  for fetch artist Id API
def test_fetch_tracks_expired_token_401():
     url = 'https://api.spotify.com/v1/search'
     artistName = 'A.R. Rahman'
     queryParams = {'query': artistName, 'offset': '0','limit': '20','type':'artist'}
     token = 'Bearer <Specify any expired token>'
     headers = {"Authorization": token}
     response = requests.get(url,headers=headers,params=queryParams)
     assert response.status_code == 401
     resp = json.loads(response.text)
     print('Fetch Artist Id, expired token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'The access token expired'

    

                        # Test Cases for Fetch Top Tracks API with Artist Id as Path Parameter

#This method tests the top tracks api using artist Id and stores the artists details and track id in a csv file
def  test_fetch_artists_top_tracks():
    #get the artist Id
     artistId = test_fetch_artist_id()
     url = 'https://api.spotify.com/v1/artists/'+artistId+'/top-tracks?market=in'
     headers = {"Authorization": bearerToken}
     response = requests.get(url,headers=headers)
     assert response.status_code == 200
     resp = json.loads(response.text)
     #Get the tracks array length
     tracksArrayLength = resp['tracks'].__len__()
     print('Tracks Array Length : ',tracksArrayLength)

     # generating a random number from the range of 0 to track length for index
     randomNumber = random.randint(0,tracksArrayLength-1)
     print('Generated randomNumber based on range of 0 to Track length : ',randomNumber)

     # retrieve any Artists data based on tracks index
     artistArr = resp['tracks'][randomNumber]['artists']
     print('Artist Data Array : ',artistArr)

     # Open the CSV file and perform write operation
     csvDataReader = open('artistData.csv', 'w')
     csvWriter = csv.writer(csvDataReader)
     
     counter = 0
     # Counter used to write the headers to the CSV file
        
     for eachArtist in artistArr:
          if counter == 0:
     
                # Write headers to CSV file
                csvHeaders = list(eachArtist.keys())
                csvHeaders.append('trackId')
                csvWriter.writerow(csvHeaders)
                    
           # Iterate row values and write it to CSV file
          csvRowValues= list(eachArtist.values())
          csvRowValues.append(resp['tracks'][randomNumber]['id'])
          csvWriter.writerow(csvRowValues)
          counter = counter + 1
             
     csvDataReader.close()

# This method verifies the invalid id case for top tracks API
def test_fetch_artists_top_tracks_400():
     url = 'https://api.spotify.com/v1/artists/539f3r94nfm49tn94n49f49f4nf94j/top-tracks?market=in'
     headers = {"Authorization": bearerToken}
     response = requests.get(url,headers=headers)
     assert response.status_code == 400
     resp = json.loads(response.text)
     print('Artists Top Tracks API, invalid id error Response : ',resp)  
     assert resp['error']['status'] == 400
     assert resp['error']['message'] == 'invalid id'

# This method verifies the 401 code by ignoring the token in url for top tracks API
def test_fetch_artists_top_tracks_no_token_401():
     artistId = test_fetch_artist_id()
     url = 'https://api.spotify.com/v1/artists/'+artistId+'/top-tracks?market=in'
     response = requests.get(url)
     assert response.status_code == 401
     resp = json.loads(response.text)
     print('Artists Top Tracks API, no token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'No token provided'

# This method verifies the 401 code by passing expired token in url for top tracks API
def test_fetch_tracks_expired_token_401():
     artistId = test_fetch_artist_id()
     url = 'https://api.spotify.com/v1/artists/'+artistId+'/top-tracks?market=in'
     token = 'Bearer <Specify any expired token>'
     headers = {"Authorization": token}
     response = requests.get(url,headers=headers)
     assert response.status_code == 401
     resp = json.loads(response.text)
     print('Artists Top Tracks API, expired token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'The access token expired'

                        # Test Cases for Fetch Tracks API using Track Id as Path Parameter

# This method tests the GET tracks api by fetching the track id from the csv file and verifies the API response
# with csv file data
def test_fetch_tracks():
    #Specify the CSV file path 
    filename = 'artistData.csv'
    # read csv file data and add them into list
    csvDataList= getCsvAsList(filename)
    print('CSV Data List Size : ',csvDataList.__len__())
    # Generate a random number within the range of list
    randomInt = random.randint(0,csvDataList.__len__()-1)
    print('Generated Random number : ',randomInt)
    # get the track id from csv data list
    trackId = csvDataList[randomInt].get('trackId')
    print('TrackId retrieved from csv data file :',trackId) 
      
    #pass the trackid got from csv file to endpoint
    url = 'https://api.spotify.com/v1/tracks/'+trackId
    headers = {"Authorization": bearerToken}
    response = requests.get(url,headers=headers)
    assert response.status_code == 200
    resp = json.loads(response.text)
    artistDataArr = resp['artists']
    print('Track API Artists Data :')  
    pprint.pprint(artistDataArr)
    
    # verify api artists arr size is matched with csv data arr size
    if csvDataList.__len__() == artistDataArr.__len__():
            print('Both array sizes are equal, proceeding to match the values')
            #declare a counter value
            counter =0
            for row in artistDataArr:
                for each in csvDataList:
                    # Match the API response values with data retrieved from csv file
                    if str(row['external_urls']) == each['external_urls'] and row['type'] == each['type'] and  row['href'] == each['href'] and row['id'] == each['id'] and  row['name'] == each['name'] and row['uri'] == each['uri']:
                        counter = counter + 1
            print('Final Counter Value :',counter)
            #Check whether the counter value is matched with total size of artists arr from api
            if counter==artistDataArr.__len__():
                print('API Artist Data is matching with the csv artists data')
            else:
                assert 'Artists Data from API is not matched with CSV data stored'
    else:
        assert 'Artists Array size of API is not matched with CSV Data size'


# This method verifies the invalid id case for tracks API
def test_fetch_tracks_400():
     url = 'https://api.spotify.com/v1/tracks/4565'
     headers = {"Authorization": bearerToken}
     response = requests.get(url,headers=headers)
     assert response.status_code == 400
     resp = json.loads(response.text)
     print('Track API Invalid Id Error response',resp)  
     assert resp['error']['status'] == 400
     assert resp['error']['message'] == 'invalid id'

# This method verifies the 401 code by ignoring the token in url for tracks API
def test_fetch_tracks_no_token_401():
     url = 'https://api.spotify.com/v1/tracks/4565'
     response = requests.get(url)
     assert response.status_code == 401
     resp = json.loads(response.text)
     print('Track API no token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'No token provided'

# This method verifies the 401 code by passing expired token in url for tracks API
def test_fetch_tracks_expired_token_401():
     url = 'https://api.spotify.com/v1/tracks/874914914'
     token = 'Bearer <Specify any expired token>'
     headers = {"Authorization": token}
     response = requests.get(url,headers=headers)
     assert response.status_code == 401
     resp = json.loads(response.text)
     print('Track API expired token Error Response : ',resp)  
     assert resp['error']['status'] == 401
     assert resp['error']['message'] == 'Invalid access token'

    


                                              #Utility Methods

# Function to convert a csv file to a list of dictionaries.Takes filepath as variable
def getCsvAsList(filePath):
    # Open the csv file with filepath provided and iterate over the rows to a list of dictionaries as key/value pair
    csvReader = csv.DictReader(open(filePath))
    csvAsList = []
    for eachRow in csvReader:
        csvAsList.append(eachRow)
    return csvAsList

#Function to read a txt file and return as list. Takes filepath as variable
def getTxtAsList(filepath):
     textfile = open(filepath, 'r')
     content = textfile.readlines()
     textfile.close()
     return content

    
