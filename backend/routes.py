from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify({"pictures": data}), 200

   

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
     picture = next((p for p in data if p["id"] == id), None)
     if picture:
        return jsonify({"picture": picture}), 200
     else:
        abort(404, f"Picture with ID {id} not found")
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
   existing_picture = next((p for p in data if p["id"] == id), None)
    
   if existing_picture:
        abort(302, {"Message": f"Picture with ID {id} already present"})

 
   picture_data = request.json
   if not picture_data or "url" not in picture_data:
        abort(400, {"Message": "Bad request, missing 'url' in request body"})

   
   new_picture = {"id": id, "url": picture_data["url"]}
   data.append(new_picture)

   return jsonify({"picture": new_picture}), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
   picture = next((p for p in data if p["id"] == id), None)

   if picture:
        # Extract picture data from the request body
        picture_data = request.json
        if not picture_data or "url" not in picture_data:
            abort(400, {"message": "Bad request, missing 'url' in request body"})

        # Update the picture with the incoming request
        picture["url"] = picture_data["url"]

        return jsonify({"picture": picture}), 200
   else:
        abort(404, {"message": "Picture not found"})

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
  picture = next((p for p in data if p["id"] == id), None)

  if picture:
        # Delete the item from the list
        data.remove(picture)
        return "", 204  
        abort(404, {"message": "Picture not found"})

  return jsonify({"message": "Picture deleted successfully"}), 200
