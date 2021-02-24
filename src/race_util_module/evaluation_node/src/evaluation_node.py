import rospy 
import numpy as np
from carla_msgs.msg import CarlaCollisionEvent
from popgri_msgs.msg import LocationInfo, EvaluationInfo
from geometry_msgs.msg import Vector3
from std_msgs.msg import Int16, Float32, String
import time
import pickle
import carla
import os
import datetime

class EvaluationNode:

    def __init__(self, world, role_name='ego_vehicle'):
        self.subCollision = rospy.Subscriber('/carla/%s/collision'%role_name, CarlaCollisionEvent, self.collisionCallback)
        self.subLocation = rospy.Subscriber('/carla/%s/location'%role_name, LocationInfo, self.locationCallback)
        self.subWaypoint = rospy.Subscriber('/carla/%s/waypoints'%role_name, Vector3, self.waypointCallback)
        self.pubReach = rospy.Publisher('/carla/%s/reached'%role_name, String, queue_size=1)
        self.pubScore = rospy.Publisher('/carla/%s/score'%role_name, Float32, queue_size=1)
        # self.waypoint_list = pickle.load(open('waypoints','rb'))
        self.reachedPoints = []
        self.reachedPointsStamped = []
        self.speedList = []
        self.hitObjects = set()
        self.deviationCount = 0
        self.score = 0.0
        self.location = None
        self.role_name = role_name
        self.waypoint = None

        actor_list = world.get_actors()
        env_list = world.get_environment_objects()
        self.obs_map = {}
        for actor in actor_list:
            self.obs_map[str(actor.id)] = str(actor.type_id) + '_' + str(actor.id)
        self.obs_map['0'] = 'fence'

    def locationCallback(self, data):
        self.location = data

    def collisionCallback(self, data):
        hitObj = self.obs_map[str(data.other_actor_id)]+"_at_time_"+str(datetime.timedelta(
                seconds=int(rospy.get_rostime().to_sec())))
        if hitObj in self.hitObjects:
            return

        self.hitObjects.add(hitObj)
        rospy.loginfo("Collision with {}".format(self.obs_map[str(data.other_actor_id)]))
        self.score -= 100.0

    def waypointCallback(self, data):
        self.waypoint = data

    def calculateScore(self):
        location = self.location
        waypoint = self.waypoint
        if not location or not waypoint:
            return
        x = location.location.x
        y = location.location.y 
        
        distanceToX = abs(x - waypoint.x)
        distanceToY = abs(y - waypoint.y)


        vx = location.velocity.x
        vy = location.velocity.y
        v = np.sqrt(vx*vx + vy*vy)
        if v > 0.5:
            self.speedList.append(v)
        
        # NOTE reached function; range
        if distanceToX < 8 and distanceToY < 8 and not (waypoint.x, waypoint.y) in self.reachedPoints: 
            # Reach information
            reached = String()
            reachInfo = "({:.2f}, {:.2f}) at time {}".format(waypoint.x, waypoint.y, str(datetime.timedelta(
                seconds=int(rospy.get_rostime().to_sec()))))
            reached.data = reachInfo
            self.pubReach.publish(reached)
            self.reachedPoints.append((waypoint.x, waypoint.y))
            self.reachedPointsStamped.append(reachInfo)

            vBar = np.average(self.speedList)
            if np.isnan(vBar):
                return
            self.speedList = []
            self.score += vBar

        # return self.score, self.hitObjects

    def onShutdown(self):
        fname = 'score_{}_{}'.format(self.role_name, time.asctime())
        rospy.loginfo("Final score: {}".format(self.score))
        # fname = 'score_h'
        # print("hit: ", self.hitObjects)
        f = open(fname, 'wb')
        f.write("Final score: \n".encode('ascii'))
        f.write(str(self.score/2500*100).encode('ascii') + "\n".encode('ascii'))
        f.write("Obstacle hits: \n".encode('ascii'))
        f.write('\n'.join(self.hitObjects).encode('ascii'))
        f.write("Waypoints reached: \n".encode('ascii'))
        f.write('\n'.join(self.reachedPointsStamped).encode('ascii'))
        f.close()


def run(en, role_name):
    rate = rospy.Rate(20)  # 100 Hz    
    rospy.on_shutdown(en.onShutdown)
    pubEN = rospy.Publisher('/carla/%s/evaluation'%role_name, EvaluationInfo, queue_size=1)
    while not rospy.is_shutdown():
        en.calculateScore()
        info = EvaluationInfo()
        info.score = en.score 
        info.numObjectsHit = len(en.hitObjects)
        pubEN.publish(info)
        score_ = Float32()
        score_.data = float(en.score/2500*100)
        en.pubScore.publish(score_)
        rate.sleep()

if __name__ == "__main__":
    rospy.init_node("Evaluation_Node")
    role_name = rospy.get_param("~role_name", "ego_vehicle")
    print("Start evaluating the performance of %s!"%role_name)
    os.chdir(os.path.dirname(__file__))
    cwd = os.getcwd()
    client = carla.Client('localhost', 2000)
    world = client.get_world()
    en = EvaluationNode(world, role_name=role_name)
    try:
        run(en, role_name)
    except rospy.exceptions.ROSInterruptException:
        rospy.loginfo("Shutting down the evaluation node")

