from flask import Flask, request, Response
from pymongo import MongoClient
import json


app = Flask(__name__)


try:
    client = MongoClient(host="localhost", port=27017)
    db = client.DocuSketch
except ConnectionError as ex:
    print('ERROR: Unable to connect do DB', ex)


@app.route("/", methods=["POST"])
def post_item():
    """Post method from JSON"""
    try:
        item = {request.json.get("key"): request.json.get("value")}
        db_response = db.DocuSketch.insert_one(item)
        return Response(
            response=json.dumps(
                {
                    "message": "item created",
                    "id": f"{db_response.inserted_id}"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)


@app.route("/<key>/<value>", methods=["GET"])
def get_item(key, value):
    """GET method from path (GET from JSON realized too)"""
    try:
        # key = request.json.get("key")
        # value = request.json.get("value")
        """
        TO USE GET WITH JSON:
        1) Uncomment 2 lines above
        2) get_item(key, value) -> get_item()
        3) @app.route("/<key>/<value>", methods=["GET"])
         -> @app.route("/", methods=["GET"])
        """
        data = db.DocuSketch.find_one({f"{key}": f"{value}"}, {"_id": 0})
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "can't get item"}),
            status=500,
            mimetype="application/json"
        )


@app.route("/<key>/<value>/<new_value>", methods=["PUT"])
def update_item(key, value, new_value):
    """PUT method from path (PUT from JSON realized too)"""
    try:
        # key = request.json.get("key")
        # value = request.json.get("value")
        # new_value = request.json.get("new_value")
        """
        TO USE PUT WITH JSON:
        1) Uncomment 3 lines above
        2) update_item(key, value, new_value) -> update_item()
        3) @app.route("/<key>/<value>/<new_value>", methods=["PUT"])
         -> @app.route("/", methods=["PUT"])
        """
        db_response = db.DocuSketch.update_one(
            {key: value},
            {'$set': {key: new_value}}
        )
        if db_response.modified_count == 1:
            return Response(
                response=json.dumps({"message": "item updated"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps(
                {"message": "item doesn't need to be updated"}
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "can't update item"}),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
