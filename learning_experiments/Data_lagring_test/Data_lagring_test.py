import json
from pathlib import Path

komponenter = [ #format {"id":  , "navn": , "antall": , "hyll":  }
    {"id":1  , "navn": "motstand 10kohm" , "antall": 100, "hyll": 1 },
    {"id":2  , "navn": "Arduino Nano" , "antall": 8 , "hyll": 2  },
    {"id": 3 , "navn": "kondensator", "antall": 20, "hyll": 3 },
    {"id": 4 , "navn": "nmos", "antall": 20, "hyll": 4 }
]


BASE_DIR = Path(__file__).resolve().parent 
FIL_STI = BASE_DIR / "lager.json"

with open(FIL_STI, "w") as f:
    json.dump(komponenter, f, indent=4)


with open(FIL_STI, "r") as f:
    hentet_data = json.load(f)
    print(hentet_data)


