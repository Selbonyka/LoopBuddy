### Ideas

- [ ] I could use the ox.routing.route_to_gdf(G, path)["elevation"]?.route - yes it works, but it seems there is an issue with my elevation data
- I don't like how Rs' is looking, seems a bit too rough ~700 metres between points
- - we could loosen this: if list(m_paths_storage[m].keys())[0] != candidate: # checking that the u that is alredy stored for this m is not the same as the u we are at



### Files to check

- [ ] simplification


### TO DO:
- [ ] Figure out if you wanna use node simplification, if yes, maybe make it based on badness?
- [ ] Make the paths that have the same edges filter themselves out
- [ ] from uprimerings clean up the print statements
- [ ] Maybe the sharing parametres could be made kinder in the uprime_rings.py