# pytest-spotifyapi

This repository contains base scripts to test the Spotify Rest APIs in Python - Pytest Framework

To run the tests,
        1. Update your clientid and client secret in creds.py file.
        2. Open a terminal window, make sure python and pip is installed 
        3. Install pytest via pip
        4. Once all the libs are imported, run the command pytest test_spotify_api.py



--- To see the console output, run command "pytest test_spotify_api.py -s"
![image](https://user-images.githubusercontent.com/48856699/118396256-54c74200-b66c-11eb-81fd-cc3fae2bf28a.png)


--- To generate HTML report of test execution, run command "pytest test_spotify_api.py -sv --html report.html"


 Once the tests are ran, You can notice this html report generated in root folder.
 ![image](https://user-images.githubusercontent.com/48856699/118396234-37927380-b66c-11eb-8bb9-c55296073d3b.png)

        

