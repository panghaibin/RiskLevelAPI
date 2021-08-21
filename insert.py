import pymongo
from glob import glob
from config import PATHS, MONGO_CLIENT, MONGO_DB, MONGO_FILE
from json import loads

myclient = pymongo.MongoClient(MONGO_CLIENT)
mydb = myclient[MONGO_DB]
mycol = mydb[MONGO_FILE]

for jsFile in sorted(glob(f'{PATHS}/*js'), key=lambda x: x):
    with open(jsFile) as f:
        info = loads(f.read())['data']
        mycol.insert_one(info)
myclient.close()