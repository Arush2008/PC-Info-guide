from app import app
from database import db, Fan


fan_power_usage = {
    1: 3,
    2: 3,
    3: 4,
    4: 2,
    5: 4,
    6: 3,
    7: 3,
    8: 5,
    9: 5,
    10: 3,
    11: 4,
    12: 5,
    13: 4,
    14: 5,
    15: 3,
    16: 3,
    17: 4,
    18: 5,
    19: 5,
    20: 5,
    21: 4,
    22: 5,
    23: 5,
    24: 5
}


with app.app_context():

    for fan_id, power_usage in fan_power_usage.items():

        fan = db.session.get(Fan, fan_id)

        if fan:
            fan.power_usage = power_usage

    db.session.commit()


print("Fan power usage updated successfully!")