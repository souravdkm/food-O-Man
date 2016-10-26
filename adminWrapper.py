from flask import Flask, render_template, redirect, request, session, g, flash, url_for
import adminFunc
import usrSrchByTags
import datetime
import sys
import random
import time
import askFridgeOman
import partialSearch

app = Flask(__name__)
app.secret_key = "(v&a(r(u*o%s&s#i$t!i"

@app.route("/")
def index():
    fridgInst = usrSrchByTags.readFridge()
    allIngr = usrSrchByTags.readAllIngr()
    return render_template("indexBlocks.html", fridg = fridgInst, allIngrs = allIngr)

@app.route("/create")
def create():
    return render_template("adminCreate.html", user_name="Mr. No One")

@app.route("/all_recipe")
def all_recipe():
    allRecipes = adminFunc.read()
    return render_template("viewRecipe.html", recipes=allRecipes)

@app.route("/recipe_list")
def recipe_list():
    allRecipes = adminFunc.read()
    return render_template("recipeList.html", recipes=allRecipes)

@app.route("/search_from_fridge", methods=["POST"])
def search_from_fridge():
    cookTime = request.form['cookTime']
    cookTimeInt = int(cookTime)
    print cookTimeInt
    srvngSize = request.form['srvngSize']
    srvngSizeInt = int(srvngSize)
    print srvngSizeInt
    matchReciList = askFridgeOman.askFridgeOman(cookTimeInt,srvngSizeInt)
    return render_template("recipeList.html", recipes=matchReciList)

@app.route("/search_from_usr", methods=["POST"])
def search_from_usr():
    inputFrmUsrList = []
    inputFrmUsrList.append(request.form['ing1'].lower())
    inputFrmUsrList.append(request.form['ing2'].lower())
    inputFrmUsrList.append(request.form['ing3'].lower())
    inputFrmUsrList.append(request.form['ing4'].lower())
    inputFrmUsrList.append(request.form['ing4'].lower())
    inputFrmUsrList.append(request.form['ing5'].lower())
    inputFrmUsrList.append(request.form['ing6'].lower())
    inputFrmUsrList.append(request.form['ing7'].lower())
    inputFrmUsrList.append(request.form['ing8'].lower())
    inputFrmUsrList.append(request.form['ing9'].lower())
    #print filter(None,inputFrmUsrList)
    finalUsrIpList = filter(None,inputFrmUsrList)
    if not finalUsrIpList:
        return redirect("/recipe_list")
    else:
        matchReciList = partialSearch.partial_Search(finalUsrIpList)
        #adminFunc.disconnect_db()
        #print matchReciList
        return render_template("usrIpSrch.html", recipes=matchReciList)

@app.route("/create_recipe", methods=["POST"]) 
def create_recipe():
    actvStatus = request.form['optionsRadios']
    recptitle = request.form['recpTitle']
    vegOrNot = request.form['vegOrNot']
    recpIngr = request.form['recpIngr']
    recpDesc = request.form['recpDesc']
    cusnTyp = request.form['cusnTyp']
    authrName = request.form['authrName']
    srvngSize = request.form['srvngSize']
    cookngTime = request.form['cookngTime']
    imgPath = request.form['imgPath']
    vidUrl = request.form['vidUrl']
    mealTyp = request.form['mealTyp']
    print mealTyp
    spclNotes = request.form['spclNotes']
    print spclNotes
    eveThig = request.form.getlist('munch')
    print eveThig
    nMun = 0
    eMun = 0
    if not eveThig :
        print "sorry boss"
    for eachChkdVal in eveThig:
        if int(eachChkdVal) == 0 :
            nMun = 1
        if int(eachChkdVal) == 1 :
            eMun = 1
    
    ingsListforSearch = []
    ingsQtyDict = {}
    ingsCriDict = {}
    ingQtyList = recpIngr.split('\r')
    
    for sngleIngDetails in ingQtyList:
        
            snglIngAllValsList = sngleIngDetails.split(':')
            qty = snglIngAllValsList[0].strip(' \t\n\r')
            uom = snglIngAllValsList[1].strip(' \t\n\r')
            massOrVolChk = snglIngAllValsList[2].strip(' \t\n\r')
            snglIngr = snglIngAllValsList[3].strip(' \t\n\r')
            criChk = snglIngAllValsList[4].strip(' \t\n\r')
            
            ingsListforSearch.append(snglIngr)
            ingsQtyDict.update({snglIngr:{qty:uom}})
            ingsCriDict.update({snglIngr:criChk})

    notesList = spclNotes.split(',')
    
    savRcpCol ={"_id": random.randrange(1000,9999), "views" : 0, "createDate" :  time.asctime( time.localtime(time.time())),
                "actvStatus" : int(actvStatus), "recptitle" : recptitle, "vegOrNot" : vegOrNot, "recpDesc" : recpDesc, "ingsListforSearch" : ingsListforSearch,
                "cusnTyp" : cusnTyp, "authrName" : authrName, "srvngSize" : srvngSize, "cookngTime" : cookngTime, "imgPath" : imgPath, "vidUrl" : vidUrl,
                "ingQtyDict" : ingsQtyDict, "ingsCriDict" : ingsCriDict, "spclNotes" : notesList, "nghtMunch" : nMun ,"evngMunch" : eMun ,"mealTyp" : mealTyp ,"updateDateList" : [], "viewsDateList" : []}
    
    adminFunc.save_recipe(savRcpCol)
    return redirect("/all_recipe")

@app.route("/recipe/<int:id>", methods=["GET"])
def view_recipes(id):
    recipe_from_db = adminFunc.get_recipe(id)
    return render_template("viewRecipe.html", recipes=recipe_from_db)

@app.route("/recipe/<int:id>", methods=["POST"])
def actvStatusChange(id):
    adminFunc.statusChng_recipe(id)
    return redirect("/all_recipe")

@app.route("/snglRecipe/<int:id>", methods=["GET"])
def view_sngleRecipe(id):
    recipe_from_db = adminFunc.readById(id)
    return render_template("singleRecipe.html", recipes=recipe_from_db)

@app.route("/searchByIngr/<ingrd>", methods=["GET"])
def search_ByIngr(ingrd):
    recipe_from_db = usrSrchByTags.searchByIng(ingrd)
    flash('Fridge-O-Man brings you all the ' + ingrd + ' recipes')
    return render_template("recipeList.html", recipes=recipe_from_db)

@app.route("/searchVegOrNonVeg/<vornv>", methods=["GET"])
def search_VegOrNonVeg(vornv):
    recipe_from_db = usrSrchByTags.searchByVegOrNonVegRecipes(vornv)
    flash('Fridge-O-Man brings you all the ' + vornv + ' recipes')
    return render_template("recipeList.html", recipes=recipe_from_db)

@app.route("/searchByCuisine/<cusntyp>", methods=["GET"])
def search_cusn(cusntyp):
    recipe_from_db = usrSrchByTags.searchByCuisine(cusntyp)
    flash('Fridge-O-Man brings you all the ' + cusntyp + ' recipes')
    return render_template("recipeList.html", recipes=recipe_from_db)

@app.route("/searchByMealTyp/<mealtyp>", methods=["GET"])
def search_MealTyp(mealtyp):
    recipe_from_db = usrSrchByTags.searchByMealTyp(mealtyp)
    flash('Fridge-O-Man brings you all the ' + mealtyp + ' recipes')
    return render_template("recipeList.html", recipes=recipe_from_db)

@app.route("/searchBySrvngTime/<srvngtime>", methods=["GET"])
def search_srvngTime(srvngtime):
    recipe_from_db = usrSrchByTags.searchBySrvngTime(1,30)
    flash('Fridge-O-Man brings you all the recipes cooked within' + srvngtime + 'mins' )
    return render_template("recipeList.html", recipes=recipe_from_db)

if __name__ == "__main__":
    app.debug = True
    app.run()
