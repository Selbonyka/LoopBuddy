from flask import Blueprint, render_template,request, jsonify, session, send_from_directory, abort
import uuid
import pickle
import os
import time
from cachetools import TTLCache
import shutil



from main import main
from visualization.visualization import route_visualization
from utils.gpxing import paths_to_gpx

# im annoyed will fix the autodelete later - i don't even care that much i might as well just ignore it but sure
# i need to separate the error functions


views = Blueprint(__name__,"views")



# Managing sessions:
user_cache = TTLCache(maxsize=1000, ttl=900)



@views.route("/")
def home():
    return render_template("home.html")

# Handle map clicks
@views.route('/clicked', methods=['POST'])
def store_clicked_point():

    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")
    # session['data'] = request.get_json()
    # lat =  session['data'].get("lat")
    # lng =  session['data'].get("lng")

    print(f"Clicked point received: ({lat}, {lng})")

    return jsonify({"status": "clicked received"})

@views.route("/create-route", methods=["POST"])
def create_route():
    saving_directory = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/gpx_files/"

    graph_filepath = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/preloadedmap/Wien.pkl"

    # Loading the graph
    print("\nLoading the graph!\n")
    with open(graph_filepath, "rb") as f:
        G = pickle.load(f)
    print("Graph loaded succesfully!\n")

    data = request.get_json()
    print("REQUEST DATA:", data)

    lat = data.get("lat")
    lng = data.get("lng")

    distance = float(data.get("distance"))
    elevation_target = float(data.get("elevation_target"))
    pavement_preference = data.get("pavement_preference")
    stoplight_preference = data.get("stoplight_preference")
    steps_preference = data.get("steps_preference")
    elevation_error = float(data.get("elevation_error"))
    sharing_allowance = float(data.get("sharing_allowance"))
    distance_error = float(data.get("distance_error"))
    stoplight_penalty = float(data.get("stoplight_penalty"))
    steps_penalty = float(data.get("steps_penalty"))
    pavement_penalty = float(data.get("pavement_penalty"))
    alpha = float(data.get("alpha"))
    node_simplification_status = data.get("node_simplification_status")
    print('node_simplification_status',node_simplification_status)
    allowed_distance_between_nodes = int(data.get("allowed_distance_between_nodes"))

    print(type(stoplight_preference), type(steps_penalty), type(pavement_penalty), type(steps_penalty), type(alpha))

    print(f"Create route requested from: ({lat}, {lng})")

    # Calling main
    # add scaling for allowed distance between nodes

    preference_dict_sample = {"total_length": distance, "elevation_requested": elevation_target, "elevation_error": elevation_error,
                              "pavement_preferences": pavement_preference,
                              "stoplights_preference": stoplight_preference, "steps_preference":steps_preference, "sharing_allowance": sharing_allowance,
                              "node_simplification_status":node_simplification_status, "allowed_distance_between_nodes": allowed_distance_between_nodes,
                              "stoplight_penalty_strength": stoplight_penalty, "steps_penalty_strength": steps_penalty,
                              "pavement_penalty_strength": pavement_penalty, "error": distance_error,
                              "alpha": alpha}
    finalized_Paths, elevation_failure = main((lng, lat), preference_dict_sample, G)

    if elevation_failure:
        generation_status = "elevation_failure"
    elif len(finalized_Paths) == 0:
            generation_status = "failed"
    else:
        generation_status = "success"



    print("Generation status:", generation_status)

    if generation_status != "elevation_failure":

        # Assign user ID
        if "user_id" not in session:
            session["user_id"] = str(uuid.uuid4())

        user_id = session["user_id"]
        gpx_user_folder = saving_directory + user_id + "/"

        # Ensure the user's folder exists
        os.makedirs(gpx_user_folder, exist_ok=True)

        # Save GPX files in user's personal folder
        paths_to_gpx(G, finalized_Paths, gpx_user_folder)

        # Generating the html with the routes
        map_save_folder = f"/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/frontend/templates/maps/{user_id}/"
        os.makedirs(map_save_folder, exist_ok=True)
        map_path = map_save_folder + "map.html"

        route_visualization(finalized_Paths, G, map_path)

        # Saving the folders in cache:
        user_cache[user_id] = {
            "gpx_folder": gpx_user_folder,
            "map_folder": map_save_folder
        }

        print(user_cache[user_id])

        # Checking if I generated all the paths
        last_route_path = os.path.join(gpx_user_folder, f'route_{len(finalized_Paths)}.gpx')
        while not os.path.exists(last_route_path):
            time.sleep(0.1)
            print("Waiting for the files to finish generating")

    return jsonify({"status": generation_status})


# Displaying the results to the user
@views.route("/result")
def display_result():
    user_id = session.get("user_id")

    if not user_id:
        abort(403, description="Session expired or not found.")

    user_map_path = f"maps/{user_id}/map.html"  # Relative to templates folder

    return render_template(user_map_path)



@views.route('/download_gpx/<int:route_id>')
def download_gpx(route_id):
    user_id = session.get("user_id")

    if not user_id or user_id not in user_cache:
        abort(403, description="Session expired or not found.")


    user_folder = user_cache[user_id]
    filename = f'route_{route_id}.gpx'
    filepath = os.path.join(user_folder, filename)

    if os.path.exists(filepath):
        return send_from_directory(user_folder, filename, as_attachment=True)
    else:
        abort(404, description="GPX file not found.")



