import carla
import time
import numpy as np
import math

class Agent():
    def __init__(self, vehicle=None):
        self.vehicle = vehicle
        self.theta_ref = 0
        self.accum_theta_ref = 0
        self.pre_waypoints = np.zeros(shape = (30,3))
        self.pre_waypoints[0][0] = 101
        self.pre_waypoints[0][1] = 93

    def run_step(self, filtered_obstacles, waypoints, vel, transform, boundary):
        """
        Execute one step of navigation.

        Args:
        filtered_obstacles
            - Type:        List[carla.Actor(), ...]
            - Description: All actors except for EGO within sensoring distance
        waypoints 
            - Type:         List[[x,y,z], ...] 
            - Description:  List All future waypoints to reach in (x,y,z) format
        vel
            - Type:         carla.Vector3D 
            - Description:  Ego's current velocity in (x, y, z) in m/s
        transform
            - Type:         carla.Transform 
            - Description:  Ego's current transform
        boundary 
            - Type:         List[List[left_boundry], List[right_boundry]]
            - Description:  left/right boundary each consists of 20 waypoints,
                            they defines the track boundary of the next 20 meters.

        Return: carla.VehicleControl()
        """
        # Actions to take during each simulation step
        # Feel Free to use carla API; however, since we already provide info to you, using API will only add to your delay time
        # Currently the timeout is set to 10s
        x_ref = waypoints[0][0]
        y_ref = waypoints[0][1]
        x_b = transform.location.x
        y_b = transform.location.y
        if (self.pre_waypoints[0][0] != waypoints[0][0] or self.pre_waypoints[0][1] != waypoints[0][1]):
            self.theta_ref = np.arctan2(-self.pre_waypoints[0][1] + waypoints[0][1], -self.pre_waypoints[0][0] + waypoints[0][0])#*180/math.pi
            self.accum_theta_ref += np.rad2deg(self.theta_ref)
            # if self.accum_theta_ref < -180:
            #     self.accum_theta_ref += 360
            # elif self.accum_theta_ref > 180:
            #     self.accum_theta_ref -= 360
        
        # v_ref = 5
        # cur_grade = 0 # a grade to evaluate how many degrees turning needed to be made
        # for i in range(10):
        #     cur_grade += abs(self.theta_ref = np.arctan2(-self.pre_waypoints[i][1] + waypoints[i][1], -self.pre_waypoints[i][0] + waypoints[i][0]))
        # if (cur_grade <= ) #######to be continued


        # print('/n ppre waypoint:', pre_waypoints[0])
        self.pre_waypoints = waypoints

        theta_b = transform.rotation.yaw
        
        v_b = np.sqrt(vel.x**2 + vel.y**2 + vel.z**2)

        print('waypoints:',x_ref,',',y_ref)
        print('theta_ref:', self.theta_ref)
        print('accum_theta_ref:', self.accum_theta_ref)
        # print('position:', x_b, ',', y_b)
        print('theta_b:', theta_b)

        delta_x = math.cos(self.theta_ref)*(x_ref-x_b)+math.sin(self.theta_ref)*(y_ref-y_b)
        delta_y = -math.sin(self.theta_ref)*(x_ref-x_b)+math.cos(self.theta_ref)*(y_ref-y_b)
        delta_theta = self.accum_theta_ref - theta_b
        # delta_theta = self.theta_ref - theta_b
        delta_v = v_ref - v_b
        
        
        delta = np.array([delta_x, delta_y, delta_theta, delta_v])#.T

        k_x = 0.75
        k_y = 1
        k_v = 0
        k_theta = 0.1 # 0.1
        
        # K = np.array([[k_x[0],0,0,k_v[5]],[0,k_y[2],k_theta[0],0]])
        K = np.array([[k_x,0,0,k_v],[0,k_y,k_theta,0]])
        u = np.dot(K,delta)

        # print('waypoints:',waypoints[0])
        # print('u:', u)
        # print('v_b:', v_b)
        # # 
        # print("Reach Customized Agent")
        # time.sleep(0.1)
        control = carla.VehicleControl()
        if v_b < v_ref:
            control.throttle = 1
        elif v_b >= v_ref:
            control.brake = 1
        steer_threshold = np.pi#1.221

        control.steer = np.clip(u[1]/steer_threshold,-1,1) # /steer_threshold
        # if u[1] > steer_threshold: # 1.39
        #     control.steer = 1
        # elif u[1] < -steer_threshold:
        #     control.steer = -1
        # else:
        #     control.steer = u[1]/steer_threshold
        # print('throttle:', control.throttle)
        # print('steer:', control.steer)
        return control
