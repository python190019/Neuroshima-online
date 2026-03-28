import requests
import json

base_url = "http://127.0.0.1:5000/api/neuroshima"

post_data = {
    "x": 2,
    "y": 4,
    "frakcja": "borgo",
    "nazwa": "sztab",
    "rotacja": 3
}

print("ok\n")
response = requests.post(f"{base_url}/postaw", json=post_data)
print("POST response:", response.json())
print("\n---------------------------\n")

post_data = {
    "x": 1,
    "y": 3,
    "frakcja": "moloch",
    "nazwa": "rozprowacz",
    "rotacja": 2
}

response = requests.post(f"{base_url}/postaw", json=post_data)
# print("POST response:", response.json())
# print("\n---------------------------\n")


post_data = {
    "x": 1,
    "y": 3,
    "frakcja": "moloch",
    "nazwa": "rozprowacz",
    "rotacja": 2
}

response = requests.post(f"{base_url}/postaw", json=post_data)
# print("POST response:", response.json())
# print("\n---------------------------\n")


post_data = {
    "x": 4,
    "y": 2,
    "frakcja": "moloch",
    "nazwa": "szturmowiec",
    "rotacja": 0
}

response = requests.post(f"{base_url}/postaw", json=post_data)
# print("POST response:", response.json())
# print("\n---------------------------\n")

# response = requests.get(f"{base_url}/get_board")
# print("GET response:", response.json())

print("---------------------------------------------------------------\n\n\n\n\n")
# requests.post(f"{base_url}/bitwa")

response = requests.post(f"{base_url}/bitwa")
print("GET response:", response.json())

# response = requests.get(f"{base_url}/get_board")
# print("GET response:", response.json())