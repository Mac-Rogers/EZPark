import requests

# Replace with your OpenCage API key
OPENCAGE_API_KEY = '02780a04cad143838610f6a470919f90'

# Replace with your IPinfo API key
IPINFO_API_KEY = 'da2db3202fd6b2a99f74a8c0d77ef0b0'

def get_coordinates(place_name):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={OPENCAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        coordinates = data['results'][0]['geometry']
        return coordinates['lat'], coordinates['lng']
    else:
        raise Exception(f"Unable to find coordinates for {place_name}")

def place_to_ip(place_name):
    try:
        latitude, longitude = get_coordinates(place_name)
        print(f"Coordinates for {place_name}: {latitude}, {longitude}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    place_name = input("Enter the place name: ")
    place_to_ip(place_name)
