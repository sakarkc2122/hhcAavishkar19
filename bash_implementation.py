import os
test = os.system("python test_03.py")
#print(test)
test_01 = test.split(" ")
print(test_01)

if "S" in test:
    print("helloworld")
else:
    print("you made a mistake")