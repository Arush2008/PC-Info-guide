from app import app
from database import db, GPU


gpu_performance_scores = {
    1: 150,   # RTX 5090
    2: 125,   # RX 7900 XTX
    3: 90,    # RTX 5070
    4: 112,   # RX 9070 XT
    5: 110,   # RX 7900 XT
    6: 88,    # RX 7900 GRE
    7: 95,    # RX 7800 XT
    8: 82,    # RX 7700 XT
    9: 58,    # RX 7600 XT
    10: 52,   # RX 7600
    11: 65,   # RX 6750 XT
    12: 52,   # RX 6650 XT
    13: 45,   # RX 6600
    14: 140,  # RTX 4090
    15: 112,  # RTX 4080
    16: 115,  # RTX 4080 Super
    17: 100,  # RTX 4070 Ti SUPER
    18: 90,   # RTX 4070 SUPER
    19: 72,   # RTX 4060 Ti 16GB
    20: 68,   # RTX 4060 Ti 8GB
    21: 60,   # RTX 4060
    22: 38,   # RTX 3050
    23: 85,   # RTX 4070
    24: 58,   # Arc A770
    25: 48,   # Arc A750
    26: 38,   # Arc A580
    27: 25,   # Arc A380
    28: 15,   # Arc A310
    29: 65,   # Arc B580
    30: 55,   # Arc Pro A60
    31: 68,   # RTX 5060
    32: 78,   # RTX 5060 Ti
    33: 55,   # RTX 5050
    34: 96,   # RTX 3090
    35: 102,  # RTX 3090 Ti
    36: 98,   # RTX 3080 Ti
    37: 90,   # RTX 3080 12GB
    38: 85,   # RTX 3080 10GB
    39: 72,   # RTX 3070 Ti
    40: 68,   # RTX 3070
    41: 65,   # RTX 3060 Ti
    42: 50,   # RTX 3060
    43: 105,  # RX 6950 XT
    44: 100,  # RX 6900 XT
    45: 95,   # RX 6800 XT
    46: 82,   # RX 6800
    47: 70,   # RX 6700 XT
    48: 55    # Arc B570
}

with app.app_context():

    for gpu_id, score in gpu_performance_scores.items():
        gpu = GPU.query.get(gpu_id)

        if gpu:
            gpu.performance_score = score

    db.session.commit()

print("GPU performance scores updated successfully!")
