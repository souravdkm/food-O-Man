#askFridgeOman.py

from pymongo import MongoClient
import math

global con
global db
global fridgeIns
global recipcol

#The connect_db() works to connect the database and collections--recipes, fridgeInstances
def connect_db():
    global con
    global db
    global recipcol
    global fridgeIns
    con = MongoClient('mongodb://souravmohanty:fman15@ds059654.mongolab.com:59654/fridgeoman')
    db = con.fridgeoman
    recipcol = db.recipes
    fridgeIns = db.fridgeInstances
    return

#askFridgeOman: works to search based on the ingredients in user's fridge(including ingredients and respect quantity)
#parameters:
#cookT: cooking time, optional
#UServeSize: serving size, optional
#SEARCH CRITERIA(the matching recipes criteria):
#cooking time is not greater than cookT
#gredients's required quantity is not greater than the quantity in user's fridge(quantity is depending on serving size)
#the number of matching ingredients m
#the number of ingredients in recipe n
# m >= roundUp(0.5*n)
def askFridgeOman(cookT, UServeSize):

    #call the function to connect to the database
    connect_db()
    global fridgeIns
    global recipcol
    
    #get the current fridgeInstance for the user from the database which will be used in searching
    fridgeInstanceCursor = fridgeIns.find({'curr': 0})
    
    #convert cursor to dict
    fridgeInstance = list(fridgeInstanceCursor)
    fridgeInstance = fridgeInstance[0]
    
    #create a list to save the matching recipes
    matchList = []
    
    #set default serving size
    if UServeSize == 0:
        UServeSize = 2
    
    #use the embedded '$setIntersection' operater in mongodb to get a intersection part(common ingredients) between the fridgeinstance and every recipe
    interSectionList = recipcol.aggregate( [
        {
            '$project': { 'interSection': { '$setIntersection': [ fridgeInstance.get('ingsList'), '$ingsListforSearch']}}
            }
        ])

    #for every recipe, check if the intersection part meets the criteria
    for item in interSectionList:

        # get the number the common ingredients 
        interLen = len(item.get('interSection'))
        if interLen > 0:
            id = item.get('_id')
            maReciCursor = recipcol.find( { '_id': id})

            #get the number of recipe ingredients
            ingsNum = len(maReciCursor.distinct('ingsListforSearch'))

            #get the recipe
            maReci = list(maReciCursor)
            maReci = maReci[0]
            
            # set the serving size factor, used to mutiply quantity
            # quantity required is depending on serving size
            serveSizeFactor = float(UServeSize)/float(maReci.get('srvngSize'))
            
            if interLen >= math.ceil(ingsNum*0.5):
                
                if cookT != 0:
                    if int(maReci.get('cookngTime')) <= cookT:
                        matchIngs = item.get('interSection')
                        matchIngs1 = matchIngs
                        x = len(matchIngs)
                        
                        # compare each ingredient's quantity
                        for matchIng in matchIngs[0:x]:
                            
                            #get the ingredient quantity in the fridgeInstance
                            ingQforFins = fridgeInstance.get(matchIng).get('qty')

                            #get the ingredient quantity in the recipe
                            ingQforReci = maReci.get('ingQtyDict').get(matchIng)
                            for key in ingQforReci:
                                ingQforReci = key

                            #compare
                            if float(ingQforFins) < float(ingQforReci)*serveSizeFactor:
                                #get rid of the ingredient whose quantity is not enought
                                matchIngs1.remove(matchIng)
                        
                        #compare the number of ingredients again    
                        if len(matchIngs1) >= math.ceil(ingsNum*0.5):
                            matchListCursor.append(maReci)
                            
                #if user has not entered a cooking time requirement, then all the cooking time is acceptable
                else:
                    matchIngs = item.get('interSection')
                    matchIngs1 = matchIngs
                    x = len(matchIngs)

                    # compare each ingredient's quantity
                    for matchIng in matchIngs[0:x]:

                        #get the ingredient quantity in the fridgeInstance
                        ingQforFins = fridgeInstance.get(matchIng).get('qty')

                        #get the ingredient quantity in the recipe
                        ingQforReci = maReci.get('ingQtyDict').get(matchIng)
                        for key in ingQforReci:
                            ingQforReci = key

                        #compare
                        if float(ingQforFins) < float(ingQforReci)*serveSizeFactor:
                            #get rid of the ingredient whose quantity is not enought
                            matchIngs1.remove(matchIng)

                    #compare the number of ingredients again
                    if len(matchIngs1) >= math.ceil(ingsNum*0.5):
                        matchList.append(maReci)
                    
                    
    return matchList






