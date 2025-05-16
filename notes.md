### Ideas

- [ ] I could use the ox.routing.route_to_gdf(G, path)["elevation"]?.route - yes it works, but it seems there is an issue with my elevation data
- I don't like how Rs' is looking, seems a bit too rough ~700 metres between points
- - we could loosen this: if list(m_paths_storage[m].keys())[0] != candidate: # checking that the u that is alredy stored for this m is not the same as the u we are at



### Files to check

- [ ] simplification



### TO DO:
- [ ] Figure out if you wanna use node simplification, if yes, maybe make it based on badness?
- [x] Make the paths that have the same edges filter themselves out
- [x] from uprimerings clean up the print statements
- [ ] Maybe the sharing parametres could be made kinder in the uprime_rings.py
- [ ] Add message for when the route with selected elevation was not found
- [ ] Remove the elevation grade ?
- [ ] Go over the code
- [ ] implement instructions
- [ ] test optimal settings
- [x] add node simplification settings
- [ ] Consider if it possible to load the graph beforehand? the thing is the deepcopy would take longer than graph loading, maybe we could just put it in clicked? or maybe it doesn't matter
- [ ] comment out badness selected
- [ ] Cleanup the pre-processing code :D



### Notes:
- Doesn't work hat well on edges of the city where there are limited routes
- Basically only need stuff in env yml, but osmnx needs a new conda lol
  - used this command: conda create -n thesis_RunningRoutes -c conda-forge --strict-channel-priority \
  python=3.12 pandas networkx osmnx sqlite tqdm cachetools pip
  - and then pip install gpxpy

