from pymongo import MongoClient
import datetime
import sys

global con
global db
global recipcol

def connect_db():
    global con
    global db
    global recipcol
    con = MongoClient('mongodb://souravmohanty:fman15@ds059654.mongolab.com:59654/fridgeoman')
    db = con.fridgeoman
    recipcol = db.recipes
    return

def save_recipe(savRcpCol):
    global recipcol
    connect_db()
    recipcol.insert(savRcpCol)
    return

def read():
    global recipcol
    connect_db()
    allRecipes = recipcol.find()
    return allRecipes

def readById(id):
    global recipcol
    connect_db()
    getDocById = recipcol.find_one({'_id':id})
    return getDocById

def statusChng_recipe(id):
    global recipcol
    connect_db()
    getDoc = readById(id)
    if getDoc['actvStatus'] == 0 :
        recipcol.update_one({'_id':id},{'$set' : {'actvStatus' : 1}})
    elif getDoc['actvStatus'] == 1 :
        recipcol.update_one({'_id':id},{'$set' : {'actvStatus' : 0}})  
    return
