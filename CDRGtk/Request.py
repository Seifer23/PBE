import requests
import json

class RequestAle:

    def __init__(self):

        # Define the URL of the PHP script
        self.login_url = 'http://192.168.22.184/login.php/'
        self.url = 'http://192.168.22.184/api3.php/'
        self.session = requests.Session()
    
    def get(self, parameters):
                
        url = self.url + str(parameters)

        # Send a GET request with authentication

        response = self.session.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (JSON data)
            return response.json()
        else:

            return None

    def login(self, username):

        response = self.session.post(self.login_url, {'student_id' : username})

        if response.status_code != 200:
            return None
        else:
            response_parsed = response.json()
            return response_parsed['name']
    
    def logout(self):

        self.session.cookies.clear()


if __name__ == "__main__":

    req = RequestAle();
    print("student_id: ", end="")
    user = input()
    response = req.login(user)
    while True:
        print("query: ", end="")
        query = input()
        result = req.get(query)
        print(result.json())
