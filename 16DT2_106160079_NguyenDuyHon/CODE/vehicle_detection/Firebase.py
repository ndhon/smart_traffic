from firebase import Firebase

config = {
	"apiKey": "AIzaSyD9wnWDtUQjcO-xkIbegBYONIgIzxHvsrc",
    "authDomain": "control-light-df769.firebaseapp.com",
    "databaseURL": "https://control-light-df769.firebaseio.com",
    "projectId": "control-light-df769",
    "storageBucket": "control-light-df769.appspot.com",
    "messagingSenderId": "390111361678",
    "appId": "1:390111361678:web:45a2452191948ed73e67df",
    "measurementId": "G-D80CG5VW3P" }
firebase = Firebase(config)

null =0
db = firebase.database()
# Pass the user's idToken to the push method
data1 = {"control": u,
		"feedback": null}
data2 = {"control": u,
		"feedback": null}
db.child("Lane 1").set(data1)
db.child("Lane 2").set(data2)