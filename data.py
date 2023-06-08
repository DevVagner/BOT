import os
from datetime import datetime
import json
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.cc
coll_users = db.users
coll_prices = db.prices
coll_contas = db.contas
coll_config = db.config
coll_gifts = db.gifts


def day_now():
  day_now = datetime.datetime.now()
  return day_now


def is_admin(chat_id):
  user = coll_users.find_one({"chat_id": chat_id})

  if user["is_admin"]:
    return True
  else:
    return False


def exists_user(chat_id):
  if coll_users.find_one({"chat_id": chat_id.id}):
    return True
  else:
    data = {
      "chat_id": chat_id.id,
      "name": chat_id.first_name,
      "username": chat_id.username,
      "is_admin": False,
      "balance": 0,
      "historic_cc": [],
      "historic_mix": [],
      "historic_pix": [],
      "historic_manual": [],
      "historic_full": [],
      "link": "",
      "register": datetime.today().strftime("%d/%m/%Y"),
      "select_cc": "",
      "select_flag": "",
      "select_level": "",
      "quantity": 0,
      "cc_confirm": "",
      "number_pix": 0,
      "number_card": 0,
      "number_manual": 0,
      "number_cc": 0,
      "number_mix": 0,
      "number_full": 0,
      "type_historic": 0
    }

    coll_users.insert_one(data)

    return 0
  

def data_user(chat_id):
  return coll_users.find_one({"chat_id": int(chat_id)})
