import requests
import json
from jinja2 import Template
import webbrowser

# Function to get random user data from RandomUser.me API
def get_random_user():
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]
        else:
            raise Exception("No results found in RandomUser.me API response")
    else:
        raise Exception("Failed to get data from RandomUser.me API")

# Function to get location details using OpenCage Geocoding API
def get_location_details(lat, lng, api_key):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]
        else:
            raise Exception("No results found in OpenCage Geocoding API response")
    else:
        raise Exception("Failed to get data from OpenCage Geocoding API")

def main():
    try:
        # Get random user data
        user = get_random_user()
        location = user['location']
        lat = float(location['coordinates']['latitude'])
        lng = float(location['coordinates']['longitude'])

        # Replace 'OPENCARE_API_KEY' with your actual OpenCage API key
        opencage_api_key = 'OPENCAGE_API_KEY' #api key
        location_details = get_location_details(lat, lng, opencage_api_key)

        # Print user and location details
        print("Random User Data:")
        print(json.dumps(user, indent=4))
        print("\nLocation Details:")
        print(json.dumps(location_details, indent=4))

        # Generate HTML content for the Leaflet map using Jinja2 template
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Leaflet Map</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        </head>
        <body>
            <div id="mapid" style="height: 500px;"></div>
            <script>
                var mymap = L.map('mapid').setView([{{ lat }}, {{ lng }}], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(mymap);
                L.marker([{{ lat }}, {{ lng }}]).addTo(mymap)
                    .bindPopup("{{ address }}").openPopup();
            </script>
        </body>
        </html>
        """

        address = location_details['formatted']
        template = Template(template_str)
        html_content = template.render(lat=lat, lng=lng, address=address)

        # Save HTML content to a file
        map_file = 'leaflet_map.html'
        with open(map_file, 'w') as f:
            f.write(html_content)
        print(f"Map has been saved as {map_file}")

        # Open the map in Chrome browser
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser('C:\Program Files\Google\Chrome\Application\chrome.exe'))
        webbrowser.get('chrome').open('file://' + map_file) #specify your output file location

    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    main()
