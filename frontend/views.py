from flask import Blueprint, render_template,request, jsonify, session, send_from_directory, abort
import uuid
import pickle
import os
import time


from main import main
from visualization.visualization import route_visualization
from utils.gpxing import paths_to_gpx



views = Blueprint(__name__,"views")


# Managing sessions:
user_cache = {}


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


    # Cleaning files from the directory if they exist there:
    for file in os.listdir(saving_directory):
        if file.endswith(".gpx"):
            os.remove(os.path.join(saving_directory, file))

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

    print(type(stoplight_preference), type(steps_penalty), type(pavement_penalty), type(steps_penalty), type(alpha))

    print(f"Create route requested from: ({lat}, {lng})")

    # Calling main
    # add scaling for allowed distance between nodes

    preference_dict_sample = {"total_length": distance, "elevation_requested": elevation_target, "elevation_error": elevation_error,
                              "pavement_preferences": pavement_preference,
                              "stoplights_preference": stoplight_preference, "steps_preference":steps_preference, "sharing_allowance": sharing_allowance,
                              "allowed_distance_between_nodes": 300, "stoplight_penalty_strength": stoplight_penalty,
                              "steps_penalty_strength": steps_penalty, "pavement_penalty_strength": pavement_penalty, "error": distance_error,
                              "alpha": alpha}
    finalized_Paths = main((lng, lat), preference_dict_sample, G)



    # Generating the html with the routes
    save_path = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/frontend/templates/map.html"

    route_visualization(finalized_Paths, G, save_path)

    # Generating the gpx files
    generation_status = paths_to_gpx(G,finalized_Paths,saving_directory)

    # Checking if I generated all the paths
    last_route_path = os.path.join(saving_directory, f'route_{len(finalized_Paths)}.gpx')
    while not os.path.exists(last_route_path):
        time.sleep(0.1)
        print("Waiting for the files to finish generating")

    return jsonify({"status": generation_status})


# Displaying the results to the user
@views.route("/result")
def display_result():
    return render_template("map.html")



@views.route('/download_gpx/<int:route_id>')
def download_gpx(route_id):
    folder = "/Users/sofiiashome/Documents/Studying at WU/Bachelor's Thesis/Bachelor Thesis Coding/LoopBuddy/gpx_files/"
    filename = f'route_{route_id}.gpx'
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        return send_from_directory(folder, filename, as_attachment=True)
    else:
        return abort(404, description="GPX file not found.")




# from flask import Flask, send_file, request, abort
# import io
# import gpxpy.gpx
#
#
# # Assuming you have gdfs globally or stored in the session
# @app.route("/download_gpx/<int:route_id>")
# def download_gpx(route_id):
#     if route_id < 0 or route_id >= len(gdfs):
#         abort(404)
#
#     gdf = gdfs[route_id]
#     gpx = gpxpy.gpx.GPX()
#     gpx_track = gpxpy.gpx.GPXTrack()
#     gpx.tracks.append(gpx_track)
#     gpx_segment = gpxpy.gpx.GPXTrackSegment()
#     gpx_track.segments.append(gpx_segment)
#
#     for point in gdf.geometry.iloc[0].coords:
#         gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point[1], point[0]))
#
#     gpx_str = gpx.to_xml()
#     gpx_bytes = io.BytesIO(gpx_str.encode("utf-8"))
#     return send_file(gpx_bytes, as_attachment=True, download_name=f"route_{route_id + 1}.gpx", mimetype="application/gpx+xml")
#
#
