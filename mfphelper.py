# https://github.com/coddingtonbear/python-myfitnesspal/tree/02631d3acb8fde848fdf645a8a2bbdbf73c77f92
import myfitnesspal
import datetime
import collections


def login(user, password):
    return myfitnesspal.Client(user, password)


def getMFPDiary(client, year, month, day):
    day_data = client.get_date(year, month, day)
    date = datetime.date(year, month, day)
    weight = client.get_measurements("Weight", date, date)
    if not day_data.water:
        water = 0
    else:
        water = day_data.water
    if "calories" not in day_data.totals:
        day_data.totals["calories"] = 0
    if "carbohydrates" not in day_data.totals:
        day_data.totals["carbohydrates"] = 0
    if "fat" not in day_data.totals:
        day_data.totals["fat"] = 0
    if "protein" not in day_data.totals:
        day_data.totals["protein"] = 0
    if "fiber" not in day_data.totals:
        day_data.totals["fiber"] = 0
    if not weight:
        weight = 0
    else:
        weight = list(weight.items())[0][1]
    return {
        "water": water,
        "calories": day_data.totals["calories"],
        "carbs": day_data.totals["carbohydrates"],
        "fat": day_data.totals["fat"],
        "protein": day_data.totals["protein"],
        "fiber": day_data.totals["fiber"],
        "weight": weight,
    }


# client = login("blueostrich18@gmail.com")
# data = getMFPDiary(client, 2021, 12, 27)
# print(data)

# weight = client.get_measurements("Weight")
# print(weight)
