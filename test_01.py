import cv2, time

video = cv2.VideoCapture(0)

print(video)
print(type(video))

a = 1

while True:
    a += 1
    check, frame = video.read()


    print(type(check))


    print(type(frame))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Capture', gray)
    print(type(gray))

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
print(a)
video.release()

cv2. destroyAllWindows()