# LoopBuddy




### evaluation
The evaluation folder contains everything necessary and relating to conducting the evaluation for the back-end. 

It facilitates two approaches: one based on only a single point evaluated - useful for running trial runs, 
however it doesn't provide enough data for any conclusions; and the other one accepts a list of points, which can be 
pre-selected or randomly generated using  _generate_random_coordinates_ from _generate_random_coordinates_.

The first approach for the smoothing and simplification evaluation can be found in the _single_point_evaluation_ folder. 
The corresponding results are located in _results_single_point_. Each folder denotes the distance and the settings used.
Here it is worth noting that the simplification results are split into two categories: one from 0-50m and one from 50-200m. 
In both the incremental increase in allowed distance between nodes is 5. 
In regard to smoothing results the incremental change in alpha is 0.05 from 0.5 to 1 in all three folders for the 3 distances. 


## Important

For successful execution of the front-end with session management, a secret key needs to be generated locally and stored as a variable _stored_secret_key_ in _frontend.secretkey_. It should not be shared.

 Basically only need stuff in env yml, but osmnx needs a new conda lol
  - used this command: conda create -n thesis_RunningRoutes -c conda-forge --strict-channel-priority \
  python=3.12 pandas networkx osmnx sqlite tqdm cachetools pip
  - and then pip install gpxpy