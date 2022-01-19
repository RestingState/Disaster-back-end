
''' 
YOU CAN INSERT ANY NUMBER OF SATELLITES YOU WANT
IT MAY TAKE A FEW MINUTES

I choose a year in catalog 2022 , so satellites are all active
'''


import json
from satellites_json import get_TLE, insert_sat_data
for i in range(50800,50852):
    insert_sat_data(i,json.dumps(get_TLE(i)))
