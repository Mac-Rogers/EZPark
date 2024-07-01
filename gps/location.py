class Location:
    """
    A simple class to encapsulate the relevant data fields returned by phone
    """
    def __init__(self, latitude, longitude, accuracy=None, provider=None):
        self.latitude = latitude
        self.longitude = longitude
        self.accuracy = accuracy
        self.provider = provider

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude}, accuracy={self.accuracy}, " \
               f"provider={self.provider}"

    def __str__(self):
        return f"{self.provider} - Latitude, Longitude: {self.latitude}, {self.longitude}, Accuracy: {self.accuracy}"

    def get_coord(self):
        return f"{self.latitude}, {self.longitude}"
