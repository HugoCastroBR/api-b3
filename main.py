from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
from get_data import getAllValuesFiis, getAllValuesStocks, getAllValuesEtfs, getAllValuesBdrs
from lists import fiis, bdrs, stocks, etfs
import os
from os.path import join, dirname
from dotenv import load_dotenv


app = Flask(__name__)

infoAction = {}
typeStock = ""

# Loading .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# 

@app.route("/", methods=["GET"])
def route():


    

    print(">",request.args)

    searchedItem = request.args.get('ticker').upper()

    if(searchedItem[-1] == 'F'):
        searchedItem = list(searchedItem)

        del(searchedItem[-1])
        searchedItem = ''.join(str(e) for e in searchedItem)



    if searchedItem in stocks:
        typeStock = "stock"
    elif searchedItem in fiis:
        typeStock = "fii"
    elif searchedItem in etfs:
        typeStock = "etfs"
    elif searchedItem in bdrs:
        typeStock = "bdrs"
    else :
        return {
            'error': "ticker value is null"
        }

#----------------------------- FIIs ------------------------

    if typeStock == "fii":
        
        url = requests.get(
            f"https://statusinvest.com.br/fundos-imobiliarios/{searchedItem}")
        nav = BeautifulSoup(url.text, "html5lib")
        
        infoAction = getAllValuesFiis(nav, searchedItem.upper())
        
        return jsonify(data=infoAction)

#----------------------------- Stocks ------------------------

    elif typeStock == "stock":

        url = requests.get(
            f"https://statusinvest.com.br/acoes/{searchedItem}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesStocks(nav, searchedItem.upper())
        
        return jsonify(data=infoAction)

#----------------------------- ETF ------------------------

    elif typeStock == "etfs":
        
        url = requests.get(
            f"https://statusinvest.com.br/etfs/{searchedItem}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesEtfs(nav, searchedItem.upper())

        return jsonify(data=infoAction)

# ---------------------- BDRs -------------------

    elif typeStock == "bdrs":

        url = requests.get(
            f"https://statusinvest.com.br/bdrs/{searchedItem.upper()}")
        nav = BeautifulSoup(url.text, "html5lib")

        infoAction = getAllValuesBdrs(nav, searchedItem)

        return jsonify(data=infoAction)

if __name__ == "__main__":
    PORT = os.environ.get('PORT')
    HOST = os.environ.get('HOST')
    DEBUG = os.environ.get('DEBUG')
    app.run(port=PORT, host=HOST, threaded=True,debug=DEBUG)
