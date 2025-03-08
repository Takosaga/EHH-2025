import requests

def call_api():
    url = "http://127.0.0.1:8000/detect_objects/"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("Success!")
            print(response.json())
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print("Connection error: Make sure the server is running")
        return None

if __name__ == "__main__":
    call_api()