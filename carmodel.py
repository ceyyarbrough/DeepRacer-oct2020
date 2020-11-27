# Imports
import math

def reward_function(params):
	'''
	Example of rewarding the agent to follow center line
	'''
	
	# Read input parameters
	track_width = params['track_width']
	distance_from_center = params['distance_from_center']
	all_wheels_on_track = params['all_wheels_on_track']
	steering = abs(params['steering_angle'])
	crash = params['is_offtrack']
	car_speed = params['speed']
	car_progress = params['progress']
	left = params['is_left_of_center']
	waypoints_arr = params['waypoints']
	closest_waypoints_arr = params['closest_waypoints']
	heading = params['heading']

	#etc variables
	CRASH_DETECTION = crash
	ABD_STEERING_THERSHOLD = 12.5
	DISTANCE_FROM_BORDER = 0.5 * track_width - distance_from_center

	#Initialize reward
	reward = 1.0

	#Keeps all wheels on track
	if all_wheels_on_track:
		reward *= 1.2

	#Keeps steering below threshold of 12.5 degrees
	if steering > ABD_STEERING_THERSHOLD:
		reward *= 0.8
	
	#Lowers reward when off track
	if CRASH_DETECTION == True:
		reward *= 0.5
	
	#Keeps steering between borders at 1/4 and 0.05 of half of the track
	if DISTANCE_FROM_BORDER < 0.25 and DISTANCE_FROM_BORDER > 0.05:
		reward *= 1.2
	
	#rewards for picking edge closest to center on turns
	if steering > 0 and left:
		reward *= 1.2
	elif steering < 0 and left:
		reward *= 0.8
	elif steering == 0 and track_width == 0.5:
		reward *= 1.1
	else:
		reward *= 1.0

	#rewards based on speed
	if car_speed > 3.0 and CRASH_DETECTION == False:
		reward *= 1.2
	else:
		reward *= 0.8

	#Rewards car progress
	if car_progress == 100:
		reward *= 1.5
	elif car_progress == 50:
		reward *= 0.5
	elif car_progress == 10:
		reward *= 0.1
	else:
		reward *= 0.8

	#Rewards based on angling towards next waypoint
	current_point = waypoints_arr[closest_waypoints_arr[0]]
	next_point = waypoints_arr[closest_waypoints_arr[1]]
	track_direction = math.atan2(next_point[1] - current_point[1], next_point[0] - current_point[0])
	track_degrees = math.degrees(track_direction)
	degree_diff = track_degrees - heading
	if degree_diff > 10:
		reward *= 0.8
	else:
		reward *= 1.2
	
	#provides reward to car model
	return float(reward)
