# https://pyshark.com/google-sheets-api-using-python/#creating-google-api-credentials
# https://docs.gspread.org/en/latest/user-guide.html#getting-a-cell-value

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
from time import sleep
import gspread
import mfphelper
import whoophelper
import json
import sys
import argparse
import configparser
import shutil
import os
import requests

INI = "health.ini"
TEMPLATE_INI = "health.ini.template"
SPREADSHEET_MAP = "spreadsheet_map.json"
SPREADSHEET_MAP_TEMPLATE = "spreadsheet_map.json.template"


class GoogleFitClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def test(self):
        r = requests.get("https://www.googleapis.com/fitness/v1/users/me/dataSources", headers={'Authorization': self.api_key})
        return print(r.content)



def updateMFPData(login, day, date, map, worksheet, config):
    diary = mfphelper.getMFPDiary(
        login,
        date.year,
        date.month,
        date.day,
    )
    for entry in diary:
        try:
            coord = map[day][0]["mfp"][entry]
        # For elements that you don't want to track
        except KeyError as e:
            continue

        if entry == "water":
            diary[entry] = round(float(diary[entry]) / 1000, 2)

        worksheet.update(coord, diary[entry])
        sleep(0.75)  # Limit write-speed to google sheets since there's an API rate limit


def updateWhoopData(login, day, date, map, worksheet ):
    data = whoophelper.getWhoopData( login, date, date)

    for entry in data:
        coord = map[day][0]["whoop"][entry]
        worksheet.update(coord, data[entry])


def checkIfComplete(worksheet, map):
    if worksheet.acell(map["complete"]).value == "Y":
        return True
    return False


def getMap(path):
    return json.load(open(path, "r"))


def authToSheets(creds):
    return gspread.service_account(filename=creds)


def openSheet(gc, url):
    return gc.open_by_url(url)


def openTab(sheet, tab_name):
    return sheet.worksheet(tab_name)


def getDateRange(start, end):
    delta = end - start
    dates = []

    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        dates.append(day)

    return dates


def main(args):
    config = configparser.ConfigParser()
    config.read(INI)
    tab_name = args.sheet

    map = getMap(config["gsheet"]["json"])
    gc = authToSheets(config["gsheet"]["creds"])
    gsheet = openSheet(gc, config["gsheet"]["url"])
    worksheet = openTab(gsheet, tab_name)

    if checkIfComplete(worksheet, map):
        print(
            "!!!!This tab/worksheet is marked as complete!!!! Exiting to protect the data."
        )
        sys.exit()

    start = args.start
    end = args.end
    dates = getDateRange(start, end)

    day = args.sday
    login = mfphelper.login(config["mfp"]["username"], config["mfp"]["password"])

    for d in dates:
        updateMFPData(login, str(day), d, map, worksheet, config)
        day += 1

    day = args.sday
    login = whoophelper.login(INI)

    for d in dates:
        updateWhoopData(login, str(day), str(d), map, worksheet)
        day += 1
if __name__ == "__main__":

    # Create files from template if they don't exist yet
    created_initial_files = False
    if not os.path.exists(INI):
        shutil.copyfile(TEMPLATE_INI, INI)
        print("Edit health.ini to add your creds for services!")
        created_initial_files = True

    if not os.path.exists(SPREADSHEET_MAP):
        shutil.copyfile(SPREADSHEET_MAP_TEMPLATE, SPREADSHEET_MAP)
        print("Edit spreadsheet_map.json to map the cells to the correct values you'll be importing!")
        created_initial_files = True

    if created_initial_files:
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sheet",
        type=str,
        required=True,
        help="The name of the sheet/tab, you would like insert data into. (week1)",
    )
    parser.add_argument(
        "-start",
        required=True,
        type=date.fromisoformat,
        help="Date to start pulling data from MFP and Whoop. (2021-12-29)",
    )
    parser.add_argument(
        "-end",
        required=True,
        type=date.fromisoformat,
        help="Date to end pulling data from MFP and Whoop. (2021-12-30)",
    )
    parser.add_argument(
        "-sday",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="The day of the week that you would like start filling data out on. 1 is the default but you can choose 1-7.",
    )
    args = parser.parse_args()
    main(args)


# setup variables
# package
# post to github
