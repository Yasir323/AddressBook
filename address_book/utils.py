from geopy.distance import geodesic

Number = int | float


def calculate_distance(lat1: Number, lon1: Number, lat2: Number, lon2: Number) -> float:
    """
    Helper function to calculate distance between two coordinates

    :param lat1: Latitude of first location
    :param lon1: Longitude of first location
    :param lat2: Latitude of second location
    :param lon2: Longitude of second location
    :return: Distance between 2 coordinates
    """
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    return geodesic(coord1, coord2).kilometers
