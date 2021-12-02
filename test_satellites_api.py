from satellites import get_TLE, get_satellite_position

print(get_TLE(25544))
print(get_satellite_position(25544, 41.702, -76.014, 0, 2))
