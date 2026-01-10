import json
from pathlib import Path

komponenter = [ #format {"id":  , "navn": , "antall": , "hylle":  }
    {"id":1  , "navn": "motstand 10kohm" , "antall": 100, "hylle": "1" },
    {"id":2  , "navn": "Arduino Nano" , "antall": 8 , "hylle": "2"  },
    {"id": 3 , "navn": "kondensator", "antall": 20, "hylle": "3" },
    {"id": 4 , "navn": "nmos", "antall": 20, "hylle": "4" }
]


BASE_DIR = Path(__file__).resolve().parent 
FIL_STI = BASE_DIR / "lager.json"

with open(FIL_STI, "w") as f:
    json.dump(komponenter, f, indent=4)


with open(FIL_STI, "r") as f:
    hentet_data = json.load(f)
    print(hentet_data)


