# RiskLevelAPI

[中文](README.md) | English

An API of the latest risk level regions on COVID-19 in China.

There is a frontend [here](https://covid.caduo.ml/), and visit [panghaibin/COVID-Risk-Region](https://github.com/panghaibin/COVID-Risk-Region) for more information.

## Feature
### risklevel.py

- Fetch the latest outbreak risk level data automatically from the [National Health Commission](http://bmfw.www.gov.cn/yqfxdjcx/risk.html) website and save it as a *.json* file with the file name `[update_time]-[hash_value].json` (e.g. `2022041511-b38a8084.json`).

- When new data is fetched, the `latest.json` and `info.json` files are updated in addition to saving the current data. `latest.json` always holds the latest data, and `info.json` holds the filenames of all the original json files under the `Archive` folder and the corresponding timestamp of the update time. 

### GitHub Actions

- This repository is equipped with GitHub Actions for automatic data updates, which by default fetches data every 2 hours and pushes it to the `api` branch of the repository. Visiting <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/latest.json> will keep you up to date with the latest data, which can be called as an API; visiting <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/info.json> to get the corresponding information on the historical data stored in this repository

### run.py

- The script will automatically fetch the latest data and push it to the `api` branch of the git repository. The script can be deployed to a server and run on the server, which can be used to automatically update the data. The git repository can be customized.

## Usage

- Clone the repo to local and run *risklevel.py*, then the outcome as *.json* files will be stored in the `Archive` folder.

- Or fork this repository and enable GitHub Actions to automatically update the risk level data every 2 hours and push to the `api` branch of the repository.

- You can also set up a cron job on the server to run the *run.py* script to update the risk level data, and push to the specified repository automatically.

## About the *token* and *key* in the code

When making the request to acquire the data, you may notice there are some appeared private auth-keys like `token` or `key` in the code. Those are just clear texts in the JavaScript code of that website. Feel free to use.

## The API version equipped with GitHub Actions

This API version is based on [@KaikePing's](https://github.com/KaikePing/RiskLevel) original version, and adds the auto-update function based on GitHub Actions. You can use it as an API.
