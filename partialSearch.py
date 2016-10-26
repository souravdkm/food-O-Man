from pymongo import MongoClient
import math

global con
global db
global recipcol

#The connect_db() works to connect the database and collection--recipes
def connect_db():
    global con
    global db
    global recipcol
    con = MongoClient('mongodb://souravmohanty:fman15@ds059654.mongolab.com:59654/fridgeoman')
    db = con.fridgeoman
    recipcol = db.recipes
    return

#The partial_Search(searchList) works to search for the recipes based on the ingredients list
#parameter--searchList: this is a list of ingredients user entered
#Match criteria:
#The number of match ingredients should be equal or greater than the nearest larger integer of 70% of number of ingredients in the recipe
#assume recipe has n ingrediants,
#there are m ingredients in searchList match the recipe ingredients
#keep the recipe when m >= roundUp(0.7*n)
# RETURN: a list of matching recipes
def partial_Search(searchList):
    
    #call the function to connect to the database
    connect_db()
    global recipcol
    #create a list to save the cursors point to the matching recipes
    matchListCursor = []

    #use the embedded '$setIntersection' operater in mongodb to get a intersection part(common ingredients) between the searchList and every recipe
    interSectionList = recipcol.aggregate( [
        {
            '$project': { 'interSection': { '$setIntersection': [ searchList, '$ingsListforSearch']}}
            }
        ])
    
    #for every recipe, check if the intersection part meets the criteria
    for item in interSectionList:
        # get the number the common ingredients 
        interLen = len(item.get('interSection'))
        if interLen > 0:
            id = item.get('_id')
            maReci = recipcol.find( { '_id': id})
            #get the number of recipe ingredients
            ingsNum = len(maReci.distinct('ingsListforSearch'))
            # compare base on the criteria
            if interLen >= math.ceil(ingsNum*0.7):
                matchListCursor.append(maReci)

    #convert cursor list to array, which we can pass to views
    matchList = []
    for recipeCursor in matchListCursor:
        matchList.append(list(recipeCursor))
        
 
    
    return matchList
            

  


