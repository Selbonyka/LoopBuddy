# LoopBuddy

### How to run?
This repository facilitates execution of the implemented algorithms in two ways: either through running just the backend code or through launching the whole pipeline which also includes a graphical frontend.

In any case the following steps needs to be taken before execution:
1. Since OSMnx is a key part of the implementation its [installation instructions](https://osmnx.readthedocs.io/en/stable/installation.html) through **Conda** need to be followed, 
creating a new conda environment with the following command `conda create -n [name_of_env] -c conda-forge --strict-channel-priority osmnx`
   1. Here we can attest to compatibility with Python 3.12.11 as this the version on which we developed the algorithm, but support with other Python versions is unknown.
2. Then using the file environment.yml all the other required packages need to be loaded using `conda env update -n [name_of_env] -f environment.yml`


Here is where the path for the two methods of execution diverges:

#### If you would like the full version with the frontend: 
  1. In `frontend.views` update `graph_filepath` and `saving_directory`
  2. Create a file called `secretkey.py` inside the `frontend` directory which contains the variable `stored_secret_key`
  3. Execute `frontend.website_main` 
  4. Follow the link provided on the output to open the locally-hosted version of the webapp

#### If you would like to execute only the backend routing algorithm:
Please note that it is not the intended user experience, therefore it will need some tinkering. The main point is to execute main.py.
However, that means analysis of required inputs which can be found in the function's descriptionally. 
Additionally, it is important to note that the graph needs to be loaded beforehand, the function `load_graph` from `evaluation.eval_utils.overall_eval_functions` 
can be used for that purpose. For inspiration the frontend code and various evaluation code can be analyzed to gather more understanding in regard to working with main.

### System Requirements

The contents of this repo can be run on various hardware. 
During our development we worked on a machine with following characteristics and it ran smoothly:
- 64 GB of storage
- 16 GB of RAM
- 4 core CPU

Please note: There is no in-built parallelization in the pipeline, so if any is required, for example for evaluation purposes, it has to be done manually.

# Modules deep-dive
Please find some additional explanations about the modules in this repository. Recommended for reading for more in-depth understanding.

### evaluation
The evaluation folder contains everything necessary and related to conducting evaluation for the back-end. 

It facilitates two approaches: one based on only a single point evaluated - useful for running trial runs, 
however it doesn't provide enough data for any conclusions; and the other one accepts a list of points, which can be 
pre-selected or randomly generated using  `generate_random_coordinates` from `generate_random_coordinates`.

The first approach for the smoothing and simplification evaluation can be found in the `single_point_evaluation` folder. 
The corresponding results are located in `results_single_point`. Each folder denotes the distance and the settings used.
Here it is worth noting that the simplification results are split into two categories: one from 0-50m and one from 50-200m. 
In both the incremental increase in allowed distance between nodes is 5. 
In regard to smoothing results the incremental change in alpha is 0.05 from 0.5 to 1 in all three folders for the 3 distances. 

Second approach provides more data and can be found in the evaluation folder. The files have been adapted for parallelization 
by splitting different groups of distances into different files to be executed on different CPU cores, which is the reason for some files to contain the "_2" postfix

### finalizing

Contains files with functions that are used in finalizing the path in `main.py`

### frontend
Contains the files that denote frontend's behaviour as well as outputs of the generated maps for the users in `frontend/templates/maps`.
Additionally, it is the place to store the variable `stored_secret_key` in the file `secretkey.py` which enables user session management

### gpx_files
Contains gpx files generated for the users.

### graph_preprocessing
Contains the jupiter notebook that creates the pre-processed map of Vienna that can be found in the directory `preloadedmap`.
Additionally, contains the tif files containing elevation data for Vienna.

### preloadedmap
Contains the pre-processed map of Vienna with added data about stoplights, steps, pavement and elevation.

### rings
Contains files which enable `main.py` to generate the rings S, S', etc...

### utils
Various helpful functions

### visualization
Enables visualization of routes for the frontend.


---

# Thanks for reading and enjoy generating your running routes!



