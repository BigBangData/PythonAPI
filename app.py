from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
import json


class Quote(Resource):
    """Recover a specific quote with an id, 
       or get a random quote if an id is not given.
    """
    def get(self, id=0):
        if id == 0:
            return random.choice(ai_quotes), 200

        for quote in ai_quotes:
            if(quote["id"] == id):
                return quote, 200
        return "Quote not found", 404
    
    def post(self, id):
        """Receives the id of the new quote as input.
           Uses reqparse to parse the parameters that will go 
           in the body of the request (author and quote text).
        """
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        params = parser.parse_args()

        for quote in ai_quotes:
            if(id == quote["id"]):
                return f"Quote with id {id} already exists", 400

        quote = {
            "id": int(id),
            "author": params["author"],
            "quote": params["quote"]
        }

        ai_quotes.append(quote)
        return quote, 201    

    def delete(self, id):
        """Deletes a quote that is no longer inspirational.
        """
        global ai_quotes
        ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
        return f"Quote with id {id} is deleted.", 200  
   

with open('./quotes.json') as f:
    ai_quotes = json.load(f)
    
app = Flask(__name__)
api = Api(app)
    
api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
