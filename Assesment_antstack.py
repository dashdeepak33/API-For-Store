import json
import os
import sys
import base64
from flask import Flask, request, jsonify, redirect, session, Response
import requests
from datetime import datetime
import logging
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
def getResponse(status=200,data=None,mimetype='application/json',headers=None):
    responseObject = dict(timestamp=str(datetime.utcnow()),message= 'Operation Successful!' if 200 <= status <300 else 'Operation Failed!',data=data )
    return Response(json.dumps(responseObject ), status=status, mimetype=mimetype,headers=headers)

class APIStore(Resource):
    def post(self):
        try:
            requestJson = request.get_json()
            billing_info = []
            billing_info_dict = {}
            total_price = 0
            total_tax = 0
            for each_item in requestJson:
                if each_item["itemCategory"] is "Medicine" or "Food":
                    tax_price = each_item["quantity"]*each_item["price"]*5/100
                    each_item["tax_price"] = tax_price
                    each_item["tax_rate"] = "5%"
                    billing_info.append(each_item)
                if each_item["itemCategory"] is "Clothes":
                    if each_item["price"] >= 1000:
                        tax_price = each_item["quantity"]*each_item["price"]*12/100
                        each_item["tax_price"] = tax_price
                        each_item["tax_rate"] = "12%"
                    else:
                        tax_price = each_item["quantity"]*each_item["price"]*5/100
                        each_item["tax_price"] = tax_price
                        each_item["tax_rate"] = "5%"
                    billing_info.append(each_item)
                if each_item["itemCategory"] is "Music":
                    tax_price = each_item["quantity"]*each_item["price"]*5/100
                    each_item["tax_price"] = tax_price
                    each_item["tax_rate"] = "5%"
                    billing_info.append(each_item)
                if each_item["itemCategory"] is "Imported":
                    tax_price = each_item["quantity"]*each_item["price"]*18/100
                    each_item["tax_price"] = tax_price
                    each_item["tax_rate"] = "18%"
                    billing_info.append(each_item)
                if each_item["itemCategory"] is "Book":
                    each_item["tax_price"] = ""
                    each_item["tax_rate"] = ""
                    billing_info.append(each_item)
                total_price += each_item["price"]
                total_tax += each_item["tax_price"]
            if total_price >= 2000:
                billing_info_dict["tax_on_totalPrice"] = total_price*5/100
                billing_info_dict["taxRate_on_totalPrice"] = "5%"
                total_tax += total_price*5/100
            
            billing_info = sorted(billing_info, key=lambda each_item: each_item["item"])
            billing_info_dict["billing_info"] = billing_info
            billing_info_dict["total_price"] = total_price
            billing_info_dict["total_tax"] = total_tax
            billing_info_dict["Total Amount Payable"] = total_price + total_tax
            return getResponse(status=201, data=billing_info_dict)
        except Exception as e:
            logging.exception({"message": str(e)})
            return getResponse(status=500, data=str(e))


app = Flask(
    __name__,
    static_url_path="",
    static_folder="../../web/static",
    template_folder="../../web/templates",
)

CORS(app)
api = Api(app)
ma = Marshmallow(app)
app.secret_key = "Flask_secret_key"

api.add_resource(APIStore,"/integrations/APIStore")



#*driver function
if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True,
        use_reloader=False)