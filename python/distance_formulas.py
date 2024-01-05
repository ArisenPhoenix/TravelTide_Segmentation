from math import radians, sin, cos, atan2, sqrt, tan, asin


def vincenty_distance(lat1, long1, lat2, long2):
    """ More Accurate Than The Haversine Function, Also Wasn't Asked For In The Project. Initially I Was Confused And
    Believed I Was Being Asked For A Function More Accurate Than The Haversine Formula, Especially When Long Distances
    Are A Consideration. It Accounts For The Width And Height Of The Earth Which Is Hard Coded For Ease Of Use."""
    a = 6378137.0  # Equatorial radius in meters
    b = 6356752.3142  # Polar radius in meters (for WGS84 ellipsoid)
    f = 1 / 298.257223563  # Flattening
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    delta_lambda = abs(long2 - long1)

    tan_U1 = (1 - f) * tan(lat1)
    cos_U1 = 1 / sqrt(1 + tan_U1 ** 2)
    sin_U1 = tan_U1 * cos_U1

    tan_U2 = (1 - f) * tan(lat2)
    cos_U2 = 1 / sqrt(1 + tan_U2 ** 2)
    sin_U2 = tan_U2 * cos_U2

    lambda_diff = delta_lambda

    sigma = atan2(
        sqrt((cos_U2 * sin(lambda_diff)) ** 2 +
             (
             cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos(lambda_diff)) ** 2),
             sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos(lambda_diff)
             )

    alpha = asin(cos_U1 * cos_U2 * sin(lambda_diff) / sin(sigma))

    u_squared = cos_U1 ** 2 * (a ** 2 - (a ** 2 - (b ** 2) * sin_U1 ** 2)) / (b ** 2)
    A = 1 + (u_squared / 16384) * (4096 + u_squared * (-768 + u_squared * (320 - 175 * u_squared)))
    B = (u_squared / 1024) * (256 + u_squared * (-128 + u_squared * (74 - 47 * u_squared)))

    delta_sigma = B * sin(sigma) * (cos(2 * alpha + sigma) +
                                    (B / 4) * (cos(sigma) * (-1 + 2 * cos(2 * alpha + sigma) ** 2) -
                                               (B / 6) * cos(2 * alpha + sigma) * (-3 + 4 * sin(sigma) ** 2) *
                                               (-3 + 4 * cos(2 * alpha + sigma) ** 2)))

    meters = b * A * (sigma - delta_sigma)

    return meters


def haversine(lat1: float, long1: float, lat2: float, long2: float) -> float:
    """
    The Haversine Function Here Uses The Self-Named Formula To Calculate The Distance Between Two Places. It Is More
    Accurate Than The SQL Function Provided.
    :param lat1:
    :param long1:
    :param lat2:
    :param long2:
    :return:
    """
    # reassigns the variables to the converted radian values using the map function with radians as function to be
    # called
    r = 6367
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])
    # longitudinal difference
    long_diff = long2 - long1
    # latitudinal difference
    lat_diff = lat2 - lat1

    # square of half the distance between two points
    a = sin(lat_diff / 2) ** 2 + cos(lat1) * cos(lat2) * sin(long_diff / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = r * c
    return km

# if __name__ == "__main__":
#     def test():
#         distance = earth_haversine(41.507483, -99.436554, 38.504048, -98.315949)
#         print("EARTH HAVERSINE")
#         print(f"Distance between the two points: {distance:.2f} kilometers")
#         distance = vincenty_distance(41.507483, -99.436554, 38.504048, -98.315949)
#         print("VINCENTY DISTANCE")
#         print(f"Distance between the two points: {distance / 1000:.2f} kilometers")
