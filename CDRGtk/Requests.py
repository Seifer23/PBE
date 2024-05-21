import requests
import json

class Requests:

    def __init__(self):
        # Define the URL of the PHP script
        self.login_url = 'http://10.192.60.111/login.php/'
        self.url = 'http://10.192.60.111/api3.php/'
        self.session = requests.Session()
    
    def get(self, parameters):
        # Construct the full URL
        url = self.url + str(parameters)
        # Send a GET request with authentication
        response = self.session.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the parsed JSON data
            return response.json()
        else:
            return None

    def login(self, username):
        response = self.session.post(self.login_url, {'student_id': username})
        if response.status_code != 200:
            return None
        else:
            response_parsed = response.json()
            return response_parsed['name']
    
    def logout(self):
        self.session.cookies.clear()


if __name__ == "__main__":
    req = Requests()
    print("student_id: ", end="")
    user = input()
    response = req.login(user)
    while True:
        print("query: ", end="")
        query = input()
        result = req.get(query)
        if result is not None:
            print(result)
        else:
            print("Error: Unable to fetch data")
