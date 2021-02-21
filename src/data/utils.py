import argparse
import math

"""
# Sample metadata from BigEarthNet dataset
{"labels": ["Continuous urban fabric", "Discontinuous urban fabric", "Permanently irrigated land", "Rice fields"], 
"coordinates": {"ulx": 540780, "uly": 4312440, "lrx": 541980, "lry": 4311240}, "projection": 
"PROJCS[\"WGS 84 / UTM zone 29N\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,
AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],
UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],
AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",-9],
PARAMETER[\"scale_factor\",0.9996],PARAMETER[\"false_easting\",500000],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,
AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"32629\"]]", 
"tile_source": "S2A_MSIL1C_20171221T112501_N0206_R037_T29SND_20171221T114356.SAFE", "acquisition_date": "2017-12-21 11:25:01"}
"""

# From the above file zone=29, easting=540780, northing=4312440, northernHemisphere=TRUE for BigEarthNet and
# If "uly": 4312440 is positive, then northernHemisphere=TRUE, else northernHemisphere=FALSE
def convert_utm_to_latlng(zone, easting, northing):
    northernHemisphere = True
    if northing < 0:
        northernHemisphere = False

    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996
    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))
    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))
    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0
    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)
    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))
    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0
    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2
    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24
    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720
    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi
    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi
    if not northernHemisphere:
        latitude = -latitude
    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)


if __name__ == "__main__":
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')


    parser = argparse.ArgumentParser(
        description='This script provides multiple util functions which are used for data creation/processing.')
    parser.add_argument('-cull', '--convert_utm_to_latlng', default=False, type=str2bool,
                        help="whether to convert UTM to latitute and longitude")
    parser.add_argument('-z', '--zone', type=int,
                        help="what's the zone? Ex:29")
    parser.add_argument('-e', '--easting', type=int,
                        help="what's the easting? Ex: 540780")
    parser.add_argument('-n', '--northing', type=int,
                        help="what's the easting? Ex: 4312440")
    args = parser.parse_args()

    if args.convert_utm_to_latlng:
        print('convert_utm_to_latlng---START')
        print(convert_utm_to_latlng(args.zone, args.easting, args.northing))
        print('convert_utm_to_latlng---END')