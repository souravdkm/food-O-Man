from pymongo import MongoClient
import datetime
import sys
import collections

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

def connect_db_Fridge():
    global con
    global db
    global fridge
    con = MongoClient('mongodb://souravmohanty:fman15@ds059654.mongolab.com:59654/fridgeoman')
    db = con.fridgeoman
    fridge = db.fridgeInstances
    return

def readFridge():
    global con
    global db
    global fridge
    connect_db_Fridge()
    allRecipes = fridge.find({"curr": 0})
    fridgeInst = {}
    for eachrecp in allRecipes:
        for eachingr in eachrecp["ingsList"]:
            fridgeInst.update({eachingr : str(eachrecp[eachingr]["qty"])+ ' ' + str(eachrecp[eachingr]["uom"])})
    return fridgeInst

def readAllIngr():
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find()
    ingList = []
    for eachrecp in allRecipes:
        for eachingr in eachrecp["ingsListforSearch"]:
            ingList.append(eachingr)
    #uniqIngrList = list(set(ingList))
    uniqIngrList=collections.Counter(ingList)
    return uniqIngrList

def searchByIng(ingr):
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find({"ingsListforSearch": { '$in': [ingr] }})
    return allRecipes

def searchByVegOrNonVegRecipes(vegOrNon):
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find({"vegOrNot": vegOrNon})
    return allRecipes

def searchByMealTyp(mealTyp):
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find({"mealTyp": mealTyp})
    return allRecipes

def searchByCuisine(cusnTyp):
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find({"cusnTyp": cusnTyp})
    
    return allRecipes

def searchBySrvngTime(lowrLim,upprLim):
    global con
    global db
    global recipcol
    connect_db()
    allRecipes = recipcol.find({'cookngTime':{'$lte':upprLim},'cookngTime':{'$gte':lowrLim}})   
    return allRecipes

