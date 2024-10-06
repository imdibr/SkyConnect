import requests

# OpenSky Network credentials
username = 'imdibr'
password = '6s@WSK2XV6TDVjt'

# Make a request to the API
response = requests.get(
    'https://opensky-network.org/api/flights/all',
    auth=(username, password),
    params={'begin': 1630358400, 'end': 1630369200}  # Change to valid timestamps
)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())
