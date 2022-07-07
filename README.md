# RiskLevelAPI

An API of the latest risk level regions on COVID-19 in China.

自动获取最新新冠中高风险地区数据，可作为API调用

There is a frontend [here](https://covid.caduo.ml/), and visit [panghaibin/COVID-Risk-Region](https://github.com/panghaibin/COVID-Risk-Region) for more information.

此API已有对应的前端项目， [在线查看](https://covid.caduo.ml/) 。可访问 [panghaibin/COVID-Risk-Region](https://github.com/panghaibin/COVID-Risk-Region) 了解更多信息。

## Feature

- Fetch the latest outbreak risk level data automatically from the [National Health Commission](http://bmfw.www.gov.cn/yqfxdjcx/risk.html) website and save it as a *.json* file with the file name `[update_time]-[hash_value].json` (e.g. `2022041511-b38a8084.json`).

  从 [卫健委](http://bmfw.www.gov.cn/yqfxdjcx/risk.html) 网站自动下载最新的疫情风险等级数据，并保存为 *.json* 文件，文件名为`[更新时间]-[hash值].json`（如 `2022041511-b38a8084.json`）。

- When new data is fetched, the `latest.json` and `info.json` files are updated in addition to saving the current data. `latest.json` always holds the latest data, and `info.json` holds the filenames of all the original json files under the `Archive` folder and the corresponding timestamp of the update time. 

  当获取到新数据时，除了保存本次数据外，还会更新 `latest.json` 和 `info.json` 文件。`latest.json` 始终保存最新的数据，`info.json` 保存了`Archive` 文件夹下所有原始 json 文件的文件名及对应的更新时间时间戳。

- This repository is equipped with GitHub Actions for automatic data updates, which by default fetches data every 20 minutes and pushes it to the `api` branch of the repository. Visiting <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/latest.json> will keep you up to date with the latest data, which can be called as an API; visiting <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/info.json> to get the corresponding information on the historical data stored in this repository

  本项目已启用 GitHub Actions 用于数据的自动更新，默认每 20 分钟获取一次，并将其 Push 到仓库的 `api` 分支中。访问 <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/latest.json> 将始终获取到最新的数据，可作为 API 调用；访问 <https://raw.githubusercontent.com/panghaibin/RiskLevelAPI/api/info.json> 可得到本项目存储的历史数据相应信息


## Usage

Clone the repo to local and run *risklevel.py*, then the outcome as *.json* files will be stored in the `Archive` folder.

下载项目到本地，运行 *risklevel.py*，结果会保存在 `Archive` 文件夹中。

You can also fork this repository and enable GitHub Actions to automatically update the risk level data every half hour and push to the `api` branch of the repository.

也可以 Fork 本项目并启用 GitHub Actions ，默认每半小时获取一次新冠疫情风险等级数据，并将其 Push 到仓库的 `api` 分支中。

## About the *token* and *key* in the code

When making the request to acquire the data, you may notice there are some appeared private auth-keys like `token` or `key` in the code. Those are just clear texts in the JavaScript code of that website. Feel free to use.

在运行程序向网站提交请求时，你会发现代码里有一些看起来像是 `token` 或者 `key` 的秘钥。这些其实都是原网站 JavaScript 代码里的明文。直接使用即可。

## The API version equipped with GitHub Actions

This API version is based on [@KaikePing's](https://github.com/KaikePing/RiskLevel) original version, and adds the auto-update function based on GitHub Actions. You can use it as an API.

此 API 版本基于 [@KaikePing](https://github.com/KaikePing/RiskLevel) 的原版修改而来，添加了 GitHub Actions 的自动更新功能，可作为 API 供第三方调用。
