# import the necessary packages
import numpy as np
import time
import cv2
import control_light
from multiprocessing import Process
from multiprocessing import Pool
# Get output layers of darknet
labelsPath = 'yolo.names'
weightsPath = 'yolov4-tiny-custom_last.weights'
configPath = 'yolov4-tiny-custom.cfg'
#Reads a network model stored in Darknet model files.
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
#Returns count of layers of specified type.
ln = net.getLayerNames()
#Returns indexes of layers with unconnected outputs.
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

LABELS = open(labelsPath).read().strip().split("\n")
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 1),dtype="uint8")

# def centro(x, y, w, h):
#     x1 = int(w / 2)
#     y1 = int(h / 2)
#     cx = x + x1
#     cy = y + y1
#     return cx, cy

def vehicle_count(video,field):
	cap = cv2.VideoCapture(video)

	# Define the codec and create VideoWriter object
	height1 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	width1 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

	# fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# fps = int(cap.get(cv2.CAP_PROP_FPS))
	# out = cv2.VideoWriter('result.avi', fourcc, fps, (height1,width1)) 

	# Count line position
	# post_line = int(height1/1.3)

	# vehicle = 0
	# Num_vehicle=0
	# offset = 5
	confidence_setting = 0.7
	#total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	#print("Total frames in video: ",total)
	Num_vehicle = 0
	max_Num_vehicle = 0
	time_export = 15
	# start = int(time.perf_counter())
	# loop over frames from the video file stream
	while True:
		start = int(time.perf_counter())

		# read the next frame from the file
		ret, frame = cap.read() 
		# if the frame was not ret, then we have reached the end of the stream
		if frame is None:
			break
		(H, W) = frame.shape[:2]
		# construct a blob from the input frame and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes
		# and associated probabilities
		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
		net.setInput(blob)
		layerOutputs = net.forward(ln)

		# initialize our lists of detected bounding boxes, confidences,
		# and class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability)
				# of the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > confidence_setting:
					# scale the bounding box coordinates back relative to
					# the size of the image, keeping in mind that YOLO
					# actually returns the center (x, y)-coordinates of
					# the bounding box followed by the boxes' width and
					# height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top
					# and and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates, confidences, and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.6)
		#print(len(idxs))

		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# draw a bounding box rectangle and label on the frame
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				# draw a bounding box circle
				# center = centro(x,y,w,h)
				# cv2.circle(frame,center, 3, (255, 0, 0),-1)

				text = "{}: {:.2f}%".format(LABELS[classIDs[i]], 100*confidences[i])
				cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
		cv2.putText(frame, "VEHICLE COUNT : " + str(len(idxs)), (5, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

		if start%time_export==0:
			Num_vehicle = len(idxs)
			control_light.data_Thingspeak(Num_vehicle,field)
			if max_Num_vehicle<Num_vehicle:
				max_Num_vehicle=Num_vehicle
				print(max_Num_vehicle)
				# return max_Num_vehicle
			print(start)
			# if start%(time_export*4)==0:	

		# if cv2.waitKey(1) & 0xFF == ord('a'):
		# 	cv2.imshow('Out',frame)
		# 	print(len(idxs))
		# finish = time.perf_counter()
		# cv2.putText(frame, str(int(1/(finish-startrt))) +" fps", (width1-70,18), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

		# Press 'q' for exiting video
		cv2.imshow('OutputVideo',frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break 
	# release the file pointers
	cap.release()
	cv2.destroyAllWindows()
	# qreturn len(idxs)
	# return len(idxs)

if __name__ == '__main__': 
	with Pool(2) as p:
		a = p.map(vehicle_count, [('1.mp4',1),('2.mp4',2)])
	control_light.data_Firebase(a)
	# control_light.data_Thingspeak(a)
	# video1 = '1.mp4'
	# video2 = '2.mp4'
	# p1 = Process(target=vehicle_count,args=(video1,1))
	# p2 = Process(target=vehicle_count,args=(video2,2))
	# p1.start()
	# p2.start()
	# p1.join()
	# p2.join()
	
	
	