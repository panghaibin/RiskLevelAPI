# RiskLevel

![Platform](https://img.shields.io/badge/Platform-Windows%20&%20Linux-green)

Update and compare the change of risk level of regions on COVID-19 in China.  
自动更新新冠中高风险地区数据，并记录其每日变化。

## Feature

- To download risk level data from the [National Health Commission](http://bmfw.www.gov.cn/yqfxdjcx/risk.html) website and save them as *.js* files.
- 从[卫生健康委](http://bmfw.www.gov.cn/yqfxdjcx/risk.html)网站自动下载疫情风险等级数据，并保存为 *.js* 文件
- Comparing the newest data with a nearest former one in the *Archive* folder and output the differences with markers `removed` and `new` as regions being lowered or added.
- 自动比较最新的数据和 *Archive* 文件夹里上一份数据的不同，并标记 `removed` 或 `new` 以表示调低或新增的地区

## Usage

Run *risklevel.py* directly, and an outcome as a *.csv* file will be stored in the *Archive* folder.

直接运行 *risklevel.py* ，结果文件会以 *.csv* 格式直接保存在 *Archive* 文件夹里。

## About the *token* and *key* in the code

When making the request to acquire the data, you may notice there are some appeared privated auth-keys like `token` or `key` in the code. Those are just clear texts in the JavaScript code of that websit. Feel free to use.

在运行程序向网站提交请求时，你会发现代码里有一些看起来像是 `token` 或者 `key` 的秘钥。这些其实都是原网站 JavaScript 代码里的明文。直接使用即可。

## Compatible with Linux

Thanks for the contributions from [@SilenWang](https://github.com/SilenWang) for implementing an linux version, where there also carried out functions like timed requesting and mailing. Switch to **MongoDB** Branch to see.

感谢 [@SilenWang](https://github.com/SilenWang) 提供了 Linux 版本的实现。还提供了定时运行和自动发通知邮件的功能。详情请切换到 **MongoDB** 分支。
