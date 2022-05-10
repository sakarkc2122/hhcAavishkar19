import datetime
now = datetime.datetime.now()

print ("Current date and time : ")
print (type(now.strftime("%Y-%m-%d %H:%M:%S")))