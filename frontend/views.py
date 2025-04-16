from flask import Blueprint, render_template,request, jsonify, session
from main import main
import uuid






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
    # add scaling for allowed distance between nodes

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
