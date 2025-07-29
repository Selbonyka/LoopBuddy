
import gpxpy
import gpxpy.gpx


def paths_to_gpx(G, paths, saving_directory):
    """
    Turns paths into gpx files and saves them in the chosen directory
    :param G: Graph of the area
    :param paths: List of lists containing paths
    :param saving_directory: Directory to save to
    """

    gpx = gpxpy.gpx.GPX()

    for i in range(len(paths)):
        path = paths[i]
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)
        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)

        for node_id in path:
            node = G.nodes[node_id]
            lat, lon = node['y'], node['x']
            ele = node.get('elevation')
            segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))

        filename = saving_directory + "route_" + str(i+1) + ".gpx"

        with open(filename, 'w') as f:
            f.write(gpx.to_xml())
