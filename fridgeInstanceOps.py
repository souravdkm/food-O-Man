#fridgeInstanceOps.py

from pymongo import MongoClient
import datetime
import sys

global con
global db
global fridgeIns

def connect_db():
    global con
    global db
    global fridgeIns
    con = MongoClient('mongodb://souravmohanty:fman15@ds059654.mongolab.com:59654/fridgeoman')
    db = con.fridgeoman
    fridgeIns = db.fridgeInstances
    return

def disconnect_db():
    global con
    print 'Disconnecting DB'
    con.close()
    return

def save_fridge_instnc():
    connect_db()
    print 'Inserting document in Mongo'
    fridgInst = {'ingsList': ['lean beef', 'mushroom', 'butter', 'onion'], 'curr' : 0,
                 'lean beef': {'qty': 3000, 'uom': 'gram', 'pTime': '12/08/2015', 'mOrv': 0}, 
                 'mushroom': {'qty': 1000, 'uom': 'gram', 'pTime': '12/12/2015', 'mOrv': 0},
                 'butter': {'qty': 450, 'uom': 'gram', 'pTime': '12/30/2015', 'mOrv': 0},
                 'onion': {'qty': 2000, 'uom': 'gram', 'pTime': '12/15/2015', 'mOrv': 0}}
    
    fridgeIns.insert(fridgInst)
    print 'Insert complete'
    disconnect_db()
    return

if __name__ == "__main__":
    save_fridge_instnc()
    
