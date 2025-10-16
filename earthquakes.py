import requests


def get_data():
    # With requests, we can ask the web service for the data.
    # The parameters define our query:
    # - starttime/endtime: date range for earthquakes
    # - minlatitude/maxlatitude: bounding box for latitude (50.008 to 58.723)
    # - minlongitude/maxlongitude: bounding box for longitude (-9.756 to 1.67)
    # - minmagnitude: minimum magnitude of earthquakes to include
    # - orderby: sort by time ascending
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # The text is in JSON format, so we need to parse it to a Python dictionary
    data = response.json()
    
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    # In GeoJSON format, earthquakes are stored in the "features" array
    # The count is simply the length of this array
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    # In the GeoJSON structure, magnitude is at:
    # earthquake -> properties -> mag
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    # In GeoJSON, coordinates are stored as [longitude, latitude, altitude]
    coordinates = earthquake["geometry"]["coordinates"]
    return coordinates[1], coordinates[0]  # Return as (latitude, longitude)


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_magnitude = -1
    max_earthquake = None
    
    # Iterate through all earthquakes to find the one with maximum magnitude
    for earthquake in data["features"]:
        magnitude = get_magnitude(earthquake)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_earthquake = earthquake
    
    # Get the location of the strongest earthquake
    max_location = get_location(max_earthquake)
    
    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)} earthquakes")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")