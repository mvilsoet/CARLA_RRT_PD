# [GRAIC: A competition for intelligent racing](https://popgri.github.io/Race/)

Generalized RAcing Intelligence Competition (GRAIC). The goal of this competition is to record and help advance the state-of-the-art in (model-based and model-free)  as decision & control applied to tactical decision making for racing environments. 

The focus of this project repository is on planning and control, since we are provided with the ground truth perception data.

## [GRAIC Documention](https://popgri.github.io/Race/installation/) to install.

The TA's should only need our agent.py to run the code, then run it like usual

Set environment variables and launch CARLA simulator:

`export PYTHONPATH=$PYTHONPATH:{user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/carla/`

`export PYTHONPATH=$PYTHONPATH:{user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg`

`cd {user_filespace}/catkin_ws/CARLA_0.9.13/`

`./CarlaUE4.sh`

# Running our Decision & Control Algorithm (Linux):

`cd  {user_filespace}/catkin_ws/CARLA_0.9.13/PythonAPI/util`

`python3 config.py -m /Game/map_package/Maps/shanghai_intl_circuit/shanghai_intl_circuit`

Run (python3) `automatic_control_GRAIC.py`

![Screenshot_1](https://user-images.githubusercontent.com/57650580/211971279-9b16b1ab-ee7c-4768-a0b6-24a341dc10e7.png)

Video: The car ignores obstacles that are too far and doesn't need to swerve. Near the middle of the video, a pedestrian runs into the road which confuses the car a little which causes it to wobble. However, as the car gets closer to the pedestrian, the waypoint that represents the obstacle/pedestrian has a larger effect on the algorithm's choice and the car successfully swerves left. 

https://user-images.githubusercontent.com/57650580/211971269-0e5154a6-9352-48b6-8756-9f0e7cf04fa4.mp4



References: 

- [Guided Hybrid A-star Path Planning Algorithm for Valet Parking Applications](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8813752&tag=1)

- ECE484 Principles of Safe Autonomy @ UIUC
