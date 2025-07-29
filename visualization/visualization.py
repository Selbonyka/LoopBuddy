
import osmnx as ox
import folium



def generate_pastel_colors(n):
    return [f"hsl({int(i * 360 / n)}, 80%, 75%)" for i in range(n)]


def route_visualization(paths, G, save_path):
    """
    Visualizes the paths by converting them to gdfs and using folium for interactive visualization, saves an html file
    at the specified save_path.

    :param paths: paths to visualize
    :param G: Graph of the area where paths are located
    :param save_path: location to save visualization to
    """

    #Generating gdfs:
    gdfs = [ox.routing.route_to_gdf(G, r, weight="length") for r in paths]

    #Generatin the color palette:
    colors = generate_pastel_colors(len(gdfs))

    # Initializing folium map with first route:
    m = gdfs[0].explore(
        tiles="cartodbpositron",
        color=colors[0],
        style_kwds={"weight": 5, "opacity": 0.8}
    )

    # Getting the middle node info:
    middle_node_id = paths[0][int(len(paths[0]) / 4)]
    middle_point = (G.nodes[middle_node_id]["y"], G.nodes[middle_node_id]["x"]) # getting out the middle point

    # Creating the marker:
    folium.Marker(
        location=middle_point,
        popup=f'<a href="/download_gpx/{1}" target="_blank">Download Route {1}</a>',
        icon=folium.DivIcon(html=f"""
            <div style="
                width: 28px;
                height: 28px;
                background: {colors[0]};
                border: 2px solid black;
                border-radius: 50%;
                text-align: center;
                line-height: 28px;
                font-weight: bold;
                font-size: 14px;
                color: black;
            ">
                {1}
            </div>
        """)
    ).add_to(m)


    # Adding the other paths:
    for i, (gdf, color) in enumerate(zip(gdfs[1:], colors[1:]), start=1): ## iterating over the paths and colors

        # Getting the middle node info:
        middle_node_id = paths[i][-int(len(paths[i]) / 4)]
        middle_point = (G.nodes[middle_node_id]["y"], G.nodes[middle_node_id]["x"])

        m = gdf.explore(m=m, color=color, style_kwds={"weight": 5, "opacity": 0.8})

        folium.Marker(
            location=middle_point,
            popup=f'<a href="/download_gpx/{i+1}" target="_blank">Download Route {i + 1}</a>', # +1 because the first path was already noted
            icon=folium.DivIcon(html=f"""
                <div style="
                    width: 28px;
                    height: 28px;
                    background: {color};
                    border: 2px solid black;
                    border-radius: 50%;
                    text-align: center;
                    line-height: 28px;
                    font-weight: bold;
                    font-size: 14px;
                    color: black;
                ">
                    {i+1}
                </div>
            """)
        ).add_to(m)


    m.save(save_path) # saving the html visualization





