# GRAIC: A competition for intelligent racing

Generalized RAcing Intelligence Competition (GRAIC). The goal of this competition is to record and help advance the state-of-the-art in (model-based and model-free)  as decision & control applied to tactical decision making for racing environments. 

The focus of this project repository is on planning and control, since we are provided with the ground truth perception data.

## [GRAIC Documention](https://popgri.github.io/Race/installation/) to install.

Set environment variables and launch CARLA simulator:

`export PYTHONPATH=$PYTHONPATH:{user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/carla/`

`export PYTHONPATH=$PYTHONPATH:{user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg`

`cd {user_filespace}/catkin_ws/CARLA_0.9.13/`

`./CarlaUE4.sh`

# Running our Decision & Control Algorithm (Linux):

`cd  {user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/util`

`python3 config.py -m /Game/map_package/Maps/shanghai_intl_circuit/shanghai_intl_circuit`

Run (python3) `automatic_control_GRAIC.py`


![Algorithm Diagram](https://drive.google.com/uc?export=view&id=1HkvLVc6cazbod4Udwyk30iPVfVqXC_8U)

References: 

- [Guided Hybrid A-star Path Planning Algorithm for Valet Parking Applications](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8813752&tag=1)

- ECE484 Principles of Safe Autonomy @ UIUC
