import requests
from io import BytesIO

def call_api():
    url = "http://127.0.0.1:8000/detect_objects/"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            data = response.json()
            print("Success!")
            print(data["data"])  # Print the detection results

            # Fetch the image
            image_url = "http://127.0.0.1:8000/image"
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                print("Should GET image with http://127.0.0.1:8000/image") # Display the image
            else:
                print(f"Error fetching image: {img_response.status_code}")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Connection error: Make sure the server is running")

if __name__ == "__main__":
    call_api()
