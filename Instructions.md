

Welcome to Loop Buddy!

So how do you generate the perfect looped routes for your run?

First pick all the basic settings in the box on the left:
- Distance [0,∞]: the total distance of the generated route (+- Distance error which could be specified in the advanced settings) 
- Target elevation change [0, ∞]: the target amount of all elevations on the route summed.
    - Examples
        - So if we set it to 0, with Elevation error (Advanced settings) = 0 we will get a path where there is no elevation whatsoever (impossible in reality)
        - And if it's set to something like 40 (+- 0) there might be one climb of 40 or a set of incline that total up to 40 (like 10+20+5+5)
- Surface type: the target surface type, Any serves as the neutral option
- Stoplights handling: defines how the algorithm handles stoplights, if 'avoid' there will be less of them, as the algorithm will actively avoid them, but their total absence cannot be guaranteed due to urban areas
- Steps handling: same logic as Stoplights handling


Now if you want to tinker around with the advanced settings, here's the description of what they do:
- Distance error [0,∞]: sets the error boundaries for the distance parameter 
- Elevation error [0, ∞]: sets the error boundaries for the elevation parameter
- Smoothing factor [0.5, 1]: parameter alpha from Gemsa et al. (2013) which affects how the circle-like the routes are, higher values -> more circular routes and more route options but higher execution time
- Sharing allowance [0, 1]: defines the permissible about of edge sharing (when the route goes over the same street more than once), lower values -> less routes, but they have less edge sharing
  - I wouldn't set that at 0, as in real world scenarios there is often sharing around the starting point when the starting point is not in the center of the city
- Stoplight/Steps/Pavement type penalties[1,10]: affect how the routing engine works. Higher values lead to these features being avoided/preferred more strongly, however lead to slower performance times
  - Note on the pavement preferences: sadly the OpenStreetMap is rather sparsely populated with the pavement data, so I wouldn't recommend setting the pavement type penalty too high.
- Node simplification status: Activates/Deactivates node simplification optimization, which reduces the number of nodes evaluated, by removing nodes that are too close to each other in Rs' are removed.
- Allowed distance between nodes: The minimum required distance between nodes for them not to be filtered out when node simplification optimization is activated.
