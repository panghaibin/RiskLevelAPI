# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 11:30:41 2021
@author: roselily

Modified on Fri Apr 15 14:31:50 2022
@author: panghaibin
"""

import os
import json
import time
import hashlib
import requests

# Location of Json files
PATHS = 'Archive'


def fetch_new():
    """
    Fetch the latest risk data from the API
    :return: json data
    """
    # Params from Ajax.js
    key = '3C502C97ABDA40D0A60FBEE50FAAD1DA'
    timestamp = str(int(time.time()))
    token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
    nonce = '123456789abcdefg'
    pass_header = 'zdww'
    _ = timestamp + token + nonce + timestamp
    _ = _.encode('utf-8')
    signatureHeader = hashlib.sha256(_).hexdigest().upper()
    _ = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + timestamp
    _ = _.encode('utf-8')
    wif_signature = hashlib.sha256(_).hexdigest().upper()

    # Send post requests
    url = 'http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson'
    data = {
        "appId": "NcApplication",
        "paasHeader": pass_header,
        "timestampHeader": timestamp,
        "nonceHeader": nonce,
        "signatureHeader": signatureHeader,
        "key": key
    }
    header = {
        "x-wif-nonce": "QkjjtiLM2dCratiA",
        "x-wif-paasid": "smt-application",
        "x-wif-signature": wif_signature,
        "x-wif-timestamp": timestamp,
        "Origin": "http://bmfw.www.gov.cn",
        "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
        "Content-Type": "application/json; charset=UTF-8"
    }
    r = requests.post(url, data=json.dumps(data), headers=header)
    risk_json = r.json()
    return risk_json


def save(file_path, json_data):
    # Save Json file
    with open(file_path, 'w', encoding="utf-8") as outfile:
        json.dump(json_data, outfile, ensure_ascii=False)


def main():
    data = fetch_new()
    update_time = data['data']['end_update_time']
    update_time = update_time.replace('-', '').replace(' ', '').replace('时', '')
    time_file_name = update_time + '.json'
    if not os.path.exists(PATHS):
        os.makedirs(PATHS)
    time_file_path = os.path.join(PATHS, time_file_name)
    if os.path.exists(time_file_path):
        print('File %s already exists' % time_file_name)
        return False
    save(time_file_path, data)
    print('File %s saved' % time_file_name)
    save(os.path.join(PATHS, 'latest.json'), data)
    print('File latest.json updated')
    return True


if __name__ == '__main__':
    main()
