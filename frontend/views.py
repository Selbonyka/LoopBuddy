from flask import Blueprint, render_template,request, jsonify
from main import main

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    return render_template("home.html")

# Handle map clicks
@views.route('/clicked', methods=['POST'])
def store_clicked_point():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    print(f"Clicked point received: ({lat}, {lng})")

    # Don't run main() here!
    return jsonify({"status": "clicked received"})

@views.route("/create-route", methods=["POST"])
def create_route():
    data = request.get_json()
    print("REQUEST DATA:", data)

    lat = data.get("lat")
    lng = data.get("lng")

    distance = float(data.get("distance"))
    elevation_target = float(data.get("elevation_target"))
    pavement_preference = data.get("pavement_preference")
    stoplight_preference = data.get("stoplight_preference")
    steps_preference = data.get("steps_preference")

    print(f"Create route requested from: ({lat}, {lng})")

    # Calling main

    preference_dict_sample = {"total_length": distance, "elevation_requested": elevation_target, "elevation_error": 10,
                              "pavement_preferences": pavement_preference,
                              "stoplights_preference": stoplight_preference, "steps_preference":steps_preference, "sharing_allowance": 0.3,
                              "allowed_distance_between_nodes": 300, "stoplight_penalty_strength": 1.1,
                              "steps_penalty_strength": 1.2, "pavement_penalty_strength": 1.05, "error": 60,
                              "alpha": 0.6}
    graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"
    finalized_Paths = main((lng, lat), preference_dict_sample, graph_filepath)

    print(finalized_Paths)

    return jsonify({"status": "generating route"})






