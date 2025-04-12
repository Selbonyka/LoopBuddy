from flask import Blueprint, render_template,request, jsonify

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    return render_template("home.html")

# Handle map clicks
@views.route("/clicked", methods=["POST"])
def receive_click():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    print(f"User clicked at: ({lat}, {lng})")

    # Optional: do something with the coordinates here

    return lat, lng



