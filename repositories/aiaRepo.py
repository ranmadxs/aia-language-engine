import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class AIAMessageRepository:
  aiaDB: None

  def __init__(self, connectionString):
    connectiondmr = MongoClient(connectionString)
    self.aiaDB = connectiondmr["aia-db"]

  def insertAIAMessage(self, aiaMessage):
    _id = self.aiaDB["aIAMessage"].insert_one(aiaMessage)
    return _id.inserted_id
  
  def updateAIAMessage(self, id, name):
    now = datetime.now()
    newBread = {
      "creationDate": now.strftime("%Y-%m-%d %H:%M:%S"),
      "name": name
    }
    filter = { '_id': ObjectId(id) }
    print("updated=")
    print(filter)
    self.aiaDB["aIAMessage"].update_one(filter, {'$push': {'breadcrumb': newBread}})
    #self.aiaDB["aIAMessage"].