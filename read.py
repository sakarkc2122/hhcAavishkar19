import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="Hackathon"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT distance1,distance2 FROM ultrasonic WHERE id=(SELECT MAX(id) FROM ultrasonic)")
myresult = mycursor.fetchall()

for x in myresult:
    distance1 = x[0]
    distance2 = x[1]
distance1 = int(distance1)
distance2 = int(distance2)
if (abs(distance1-distance2)<2):
    print("Bus")
