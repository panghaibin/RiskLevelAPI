# -*- coding: utf-8 -*-

import os, json, time, requests, hashlib
from datetime import datetime
import pandas as pd 
import pymongo, schedule, zmail

from config import PATHS, URL, MONGO_CLIENT, MONGO_DB, MONGO_FILE
from passwd import passwd, account, receiver


def loading_new():
    '''
    Loading and saving the risk-level data
    '''
    # Parms from Ajax.js
    key = '3C502C97ABDA40D0A60FBEE50FAAD1DA'
    timestamp = str(int(time.time()))
    token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
    nonce = '123456789abcdefg'
    passid = 'zdww'
    temp = timestamp + token + nonce + timestamp
    temp = temp.encode('utf-8')
    signatureHeader = hashlib.sha256(temp).hexdigest().upper()
    temp = timestamp + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + 'QkjjtiLM2dCratiA' + timestamp
    temp = temp.encode('utf-8')
    zdwwsignature = hashlib.sha256(temp).hexdigest().upper()
    
    # Send post requests
    data = {"appId":"NcApplication",
            "paasHeader":passid,
            "timestampHeader":timestamp,
            "nonceHeader":nonce,
            "signatureHeader":signatureHeader,
            "key":key}
    header = {"x-wif-nonce": "QkjjtiLM2dCratiA",
              "x-wif-paasid": "smt-application",
              "x-wif-signature": zdwwsignature,
              "x-wif-timestamp": timestamp,
              "Origin": "http://bmfw.www.gov.cn",
              "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
              "Content-Type": "application/json; charset=UTF-8"}
    r = requests.post(URL, data = json.dumps(data), headers=header)
    
    # return fetched data
    return r.json()['data']

def dup(risk1, risk2):
    '''
    Removing duplications
    '''
    df1 = pd.DataFrame(risk1).explode('communitys').drop_duplicates()
    df2 = pd.DataFrame(risk2).explode('communitys').drop_duplicates()
    # Compare df1-the previous one with df2-the newer one
    df = df1.merge(df2, indicator=True, how='outer')
    # left_only might be item that has been removed
    # right_only might be item that was updated
    shift = df.loc[df['_merge']!='both',:]
    return(shift)    
    

def comparsion(latest, former):
    '''
    Comparison with former one
    latest for json2 
    former for json1
    return a dataframe 
    '''
    # High-risk
    risk1 = latest['highlist']
    risk2 = former['highlist']
    # Removing duplications
    shift1 = dup(risk1, risk2)
    shift1['level'] = "high"
    
    # Mid-risk
    risk1 = latest['middlelist']
    risk2 = former['middlelist']
    # Removing duplications
    shift2 = dup(risk1, risk2)
    shift2['level'] = "middle"
    
    # Merge
    shift = shift1.merge(shift2, indicator=False, how='outer')
    shift['_merge'] = shift['_merge'].astype(str)    
    shift.loc[shift['_merge']=='left_only', '_merge'] = 'removed'
    shift.loc[shift['_merge']=='right_only', '_merge'] = 'new'
    shift['date'] = former['end_update_time'][0:10]
    if len(shift)>0:
        shift.drop(['type', 'area_name'], axis=1, inplace=True)
        return shift
    else:
        return pd.DataFrame()


def send_mail(account, passwd, chgData, aInfo=None):
    '''
    use zmail to send email
    '''
    mail_content = {
        'subject': '[Auto-Mail] Risk region updated',
        'content_text': f'Risk region has been updated at {aInfo["end_update_time"]}',
    }
    if aInfo:
        jsFile = os.path.join(PATHS, f'{aInfo["end_update_time"]}.js')
        with open(jsFile, 'w') as js:
            js.write(json.dumps(aInfo))
        mail_content['attachments'] = [jsFile]
    if chgData.empty:
        mail_content['content_text'] = f'{mail_content["content_text"]}, nothing changed'
    else:
        chgList = chgData['_merge'].tolist()
        csvFile = os.path.join(PATHS, f'{aInfo["end_update_time"]}.csv')
        chgData.to_csv(csvFile, index=0)
        mail_content['attachments'] += [csvFile]
        mail_content['content_text'] = f'{mail_content["content_text"]}, {chgList.count("new")} new, {chgList.count("removed")} removed'
    #使用哪个邮箱发送邮件
    server = zmail.server(account, passwd)
    #发送给哪个邮件
    server.send_mail(receiver, mail_content)
    print(f'Mail sended to {receiver}')


def update(riskData=None):
    '''
    use loading_new to get the latest data and check it in mongoDB(use end_update_time)
    if end_update_time existed, mean saved data, discard
    else get the former record, find difference and save the latest information to mongoDB
    '''
    latest = riskData if riskData else loading_new()
    latest_time = latest['end_update_time']
    myclient = pymongo.MongoClient(MONGO_CLIENT)
    mydb = myclient[MONGO_DB]
    mycol = mydb[MONGO_FILE]
    found = list(mycol.find({'end_update_time': latest_time}))
    
    if len(found) > 0: # old
        print(f'Updating at {datetime.now().strftime("%c")}')
    else: # new
        former = list(mycol.find().sort([['_id', -1]]).limit(1))[0]
        chgData = comparsion(latest, former)
        send_mail(account, passwd, chgData, aInfo=latest)
        mycol.insert_one(latest)
    myclient.close()


if __name__ == "__main__":
    # schedule.every(10).minutes.do(update)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)

    update()
    # loading_new()
    # comparsion()