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


	
	
	# Calculate 3 markers that are at varying distances away from the center line
	marker_1 = 0.1 * track_width
	marker_2 = 0.25 * track_width
	marker_3 = 0.5 * track_width

	CRASH_DETECTION = crash
	ABD_STEERING_THERSHOLD = 12.5
	DISTANCE_FROM_BORDER = .5 * track_width - distance_from_center
	
	# Give higher reward if the car is closer to center line and vice versa
	if distance_from_center <= marker_1:
		reward = 1.0
	elif distance_from_center <= marker_2:
		reward = 0.5
	elif distance_from_center <= marker_3:
		reward = 0.1
	else:
		reward = 1e-3  # likely crashed/ close to off track

	if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
		reward = 1.0

	if steering > ABD_STEERING_THERSHOLD:
		reward *= 0.8
	
	if CRASH_DETECTION == True:
		reward *= 0.5
	
	if steering > 0 and DISTANCE_FROM_BORDER < .25 and DISTANCE_FROM_BORDER > .5:
		reward = 1.0

	if car_speed > 3.0 and CRASH_DETECTION == False:
		reward = 1.0

	if car_progress == 100:
		reward = 1.0
	elif car_progress == 50:
		reward = 0.5
	elif car_progress == 10:
		reward = 0.1
	else:
		reward *= 0.8
	return float(reward)