from firebase import Firebase
import urllib.request
import time

config = {
		"apiKey": "AIzaSyBLlDTqvYBKA8ekFzZjB53f7MaUhZu8Pwc",
    "authDomain": "signal-light-2d04c.firebaseapp.com",
    "databaseURL": "https://signal-light-2d04c.firebaseio.com",
    "projectId": "signal-light-2d04c",
    "storageBucket": "signal-light-2d04c.appspot.com",
    "messagingSenderId": "721458188123",
    "appId": "1:721458188123:web:265b3dd7e0d46a251a147e",
    "measurementId": "G-5SX35388MX"}
firebase = Firebase(config)
db = firebase.database()

def data_Thingspeak(data,field):
	myAPI = 'ALO1913Z4WJSFLJZ' 
	# URL where we will send the data, Don't change it
	baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
	if field == 1:
		conn = urllib.request.urlopen(baseURL + '&field1=%s' %data)
	else:
		conn = urllib.request.urlopen(baseURL + '&field2=%s' %data)
	# print(conn.read())
	# Closing the connection
	conn.close()

def signal_light(D1, D2):
	low = 10
	hight = 20
	if (D1<low and D2>hight): 
		x1 = 23
		d1 = 56
		x2 = 53
		d2 = 26
	elif D1>hight and D2<low:
		x1 = 53
		d1 = 26
		x2 = 23
		d2 = 56
	elif D1>hight and D2>hight:
		x1 = 56
		d1 = 59
		x2 = 56
		d2 = 59
	elif D1<low and D2<low:
		x1 = 20
		d1 = 23
		x2 = 20
		d2 = 23
	else:
		x1 = 38
		d1 = 41
		x2 = 38
		d2 = 41
	return x1, d1, x2, d2

def write_data(b):
	
	data1 = {"Lane1/green_timing": b[0],
			"Lane1/red_timing": b[1]}
	data2 = {"Lane2/green_timing": b[2],
			"Lane2/red_timing": b[3]}
	db.update(data1)
	db.update(data2)

def data_Firebase(a):
	write_data(signal_light(a[0],a[1]))

# def read_data(feedback_signal):
# 	feedback_signal = db.child("Lane1/feedback").get()
# 	print(feedback_signal.val())
# 	return feedback_signal.val()

a = [1,10]
data_Firebase(a)
# datThingspeak(a)