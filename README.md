# MFP and Whoop data into Google sheet
## Tool to get MyFitnessPal(MFP) and Whoop data into a google sheet

This tool utilizes the work of https://github.com/coddingtonbear/python-myfitnesspal/ and https://github.com/irickman/whoop-downloader

**Note:** Since myfitnesspal has an invisible captcha on their site, the `python-myfitnesspal` library authenticates using cookies from your browser.

Follow these instructions for setting up Google API Service Account: https://support.google.com/a/answer/7378726

***You must share the google sheet you are putting data into with the service account you just created in the step above. Service account email can be found in the json cred file that was downloaded***

Highly recommended to run in a [python virtual enviornment](https://docs.python.org/3/library/venv.html)

```python
pip install -r requirements.txt
```

Make sure you have your Whoop creds available and you have authenticated to myfitnesspal using the browser of your choice (be sure to use the arg `-browser` to pass in a browser name if not using chrome)

Add your data to the health.ini file
```INI
[whoop]
username=
password=

[gsheet]
json=path\to\spreadsheet_map.json
creds={location of json file
url={url of google sheet}
```

Configure your spreadsheet_map.json to match the layout of your spreadsheet. This is how the program knows what data goes in what cells.

Usage

```bash
usage: upload.py [-h] [-browser {chrome,opera,chromium,edge,firefox,safari}] -sheet SHEET -start START -end END [-sday {1,2,3,4,5,6,7}]

optional arguments:
  -h, --help            show this help message and exit
  -browser {chrome,opera,chromium,edge,firefox,safari}
                        Browser to try and load myfitnesspal cookies from
  -sheet SHEET          The name of the sheet/tab, you would like insert data into. (week1)
  -start START          Date to start pulling data from MFP and Whoop. (2021-12-29)
  -end END              Date to end pulling data from MFP and Whoop. (2021-12-30)
  -sday {1,2,3,4,5,6,7}
                        The day of the week that you would like start filling data out on. 1 is the default but you can choose 1-7.
```

```bash
python upload.py -browser firefox -sheet "Week1" -start "2021-12-27" -end "2021-12-29"
```


