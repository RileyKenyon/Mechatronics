import numpy as np
import cv2
import depthai
import consts.resource_paths
import serial

global r_sensitivity, g_sensitivity
r_sensitivity = 10;
g_sensitivity = 25;

def processImage(image):
	# Determine Masks
	global red_sensitivity, green_sensitivity
	blur = cv2.medianBlur(image,3)
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	green_mask = cv2.inRange(hsv,(60 - g_sensitivity,100,20),(60 + g_sensitivity,255,255))
	red_lower = cv2.inRange(hsv,(0,100,100),(r_sensitivity,255,255))
	red_upper = cv2.inRange(hsv,(180-r_sensitivity,100,100),(180,255,255))
	red_mask = cv2.bitwise_or(red_lower,red_upper)		# Red is bilateral

	# Refine Masks	
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	red_mask = cv2.erode(red_mask,kernel)	
	red_mask = cv2.dilate(red_mask,kernel)
	green_mask = cv2.erode(green_mask,kernel)
	green_mask = cv2.dilate(green_mask,kernel)
	
	# Determine bounding box and contours - note that top left of image is (0,0)
	g_contours,_ = cv2.findContours(green_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	r_contours,_ = cv2.findContours(red_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	pos = np.array([[None,None],[None,None]])
	if len(g_contours) is not 0:
		c = max(g_contours,key=cv2.contourArea)
		x,y,width,height = cv2.boundingRect(c)
		color = (0,255,0)
		cv2.rectangle(image,(x,y),(x+width,y+height),color,2)
		pos[0] = (x+width/2,y+height/2)
		cv2.putText(image,str(pos[0]),(int(x+width+10),int(y)+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
	if len(r_contours) is not 0:
		c = max(r_contours,key=cv2.contourArea)
		x,y,width,height = cv2.boundingRect(c)
		color = (0,0,255)
		cv2.rectangle(image,(x,y),(x+width,y+height),color,2)
		pos[1] = (x+width/2,y+height/2)
		cv2.putText(image,str(pos[1]),(int(x+width+10),int(y)+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
	return image, pos



'''
Main script - Identify location of friend or foe, annotate frame, and return location

'''
if not depthai.init_device(consts.resource_paths.device_cmd_fpath):
	print("Error Initializing device. Try to reset it.")
	exit(1)

# create pipeline for previewout stream
p = depthai.create_pipeline(config={
	'streams': 
	{
		'name': 'previewout', 
		#'max_fps': 12.0
	}, # {'name': 'depth_sipp', "max_fps": 12.0}, 
	'depth':
    	{
        	'calibration_file': consts.resource_paths.calib_fpath,
        	# 'type': 'median',
        	'padding_factor': 0.3
    	},
	'ai': 
	{
		'blob_file': consts.resource_paths.blob_fpath
	},
	'board_config':
    	{
        	'swap_left_and_right_cameras': True, # True for 1097 (RPi Compute) and 1098OBC (USB w/onboard cameras)
        	'left_fov_deg': 69.0, # Same on 1097 and 1098OBC
        	'left_to_right_distance_cm': 7.5, # Distance between stereo cameras
        	'left_to_rgb_distance_cm': 2.0 # Currently unused
    	}
})

if p is None:
	print("Error creating pipeline")
	exit(2)

# Establish serial communication
ser = serial.Serial('/dev/ttyACM0')
frame_count = 0

while True:
	data_packets = p.get_available_data_packets()
	
	for packet in data_packets:
		if packet.stream_name == 'previewout':
			data = packet.getData()
			data0 = data[0,:,:]
			data1 = data[1,:,:]
			data2 = data[2,:,:]
			frame = cv2.merge([data0,data1,data2])
			frame,position = processImage(frame)	# channel 1 is green, channel 2 is red
			if frame_count == 0:
				if position[0][0] is not None:
					command = 'G:'+str(int(position[0][0]))+','+str(int(position[0][1]))+'\n'
					ser.write(bytes(command,'UTF-8'))
					x = ser.readline()
					print(x.decode('UTF-8'))
				if position[1][0] is not None:
					command = 'R:'+str(int(position[1][0]))+','+str(int(position[1][1]))+'\n'
					ser.write(bytes(command,'UTF-8'))
					x = ser.readline()
					print(x.decode('UTF-8'))
			cv2.imshow('previewout',frame)
			frame_count = frame_count + 1
			frame_count = frame_count % 200	# Used for sending information to arduino
			
	if cv2.waitKey(1) == ord('q'):
		break

del p
ser.close()
