import math

def dot(a,b):
    return sum([x * y for [x,y] in zip(a,b)]) if len(a) == len(b) else None

def cross(a,b):
    x = a[1]*b[2] - a[2]*b[1]
    y = - (a[0]*b[2] - a[2]*b[0])
    z = (a[0]*b[1] - a[1]*b[0])
    return [x,y,z]

def norm(a):
    return math.sqrt(dot(a, a))

def normalized(a):
    return [x / norm(a) for x in a]

def dist(a, b):
    return norm([x - y for [x,y] in zip(a,b)])

class WGS84:
    @staticmethod
    def equatorialRadius():
        return 6378137.0
    @staticmethod
    def inverseFlattening():
        return 298.257223563
    @staticmethod
    def polarRadius():
        return WGS84.equatorialRadius() * (1.0 - 1.0 / WGS84.inverseFlattening())
    @staticmethod
    def a():
        return WGS84.equatorialRadius()
    @staticmethod
    def b():
        return WGS84.polarRadius()
    @staticmethod
    def radius(lat):
        return WGS84.a() * WGS84.b() / math.sqrt((WGS84.b() * math.cos(lat * math.pi / 180.0))**2 + (WGS84.a() * math.sin(lat * math.pi / 180.0))**2)
    @staticmethod
    def cartesian(lat, long):
        return [ WGS84.a() * math.cos(lat * math.pi / 180.0) * math.cos(long * math.pi / 180.0), WGS84.a() * math.cos(lat * math.pi / 180.0) * math.sin(long * math.pi / 180.0), WGS84.b() * math.sin(lat * math.pi / 180.0) ]
    @staticmethod
    def normal(lat, long):
        [x, y, z] = WGS84.cartesian(lat, long)
        tmp = [2 * x / WGS84.a()**2, 2 * y / WGS84.a()**2, 2 * z / WGS84.b()**2]
        return normalized(tmp)
    @staticmethod
    def geodesic(latLongA, latLongB):
        # NOTE: this is a small-angle approximation
        normalA = WGS84.normal(latLongA[0], latLongA[1])
        normalB = WGS84.normal(latLongB[0], latLongB[1])
        rad = (WGS84.radius(latLongA[0]) + WGS84.radius(latLongB[0])) / 2.0
        return rad * math.atan2(norm(cross(normalA, normalB)), dot(normalA, normalB))
