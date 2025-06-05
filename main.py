import cv2
import mediapipe as mp
import pyautogui as paglu
# initialize webcam
camera = cv2.VideoCapture(0)
facemesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
sw,sh = paglu.size()  # get screen width and height

if not camera.isOpened():
    print("error: camera nahi hai paglu")
    exit()

while True:
    _, frame = camera.read()  # read a frame from the webcam
    if not _:
        print("error: camera nahi hai paglu")
        break
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert frame to RGB
    results = facemesh.process(rgb_frame)  # process the frame with FaceMesh
    lm_points = results.multi_face_landmarks  # get the landmarks
    frame_height, frame_width, _ = frame.shape  # get the frame dimensions
    if lm_points:
        landmarks = lm_points[0].landmark  # get the first face landmarks
        for id, lm in enumerate(landmarks[474:478]):
            x = int(lm.x * frame_width)  # convert normalized x to pixel x
            y = int(lm.y * frame_height)  # convert normalized y to pixel y
            cv2.circle(frame, (x,y), 3, (0, 255, 0))  # draw a circle at the landmark position
            if id == 1:
                scrx = sw/frame_width * x  # calculate screen x position
                scry = sh/frame_height * y  # calculate screen y position
                paglu.moveTo(scrx, scry)  # move the mouse to the calculated position
        left_eye = [landmarks[145],landmarks[159]]
        for lm in left_eye:
            x = int(lm.x * frame_width)
            y = int(lm.y * frame_height)
            cv2.circle(frame, (x,y), 3, (0, 255, 255))  # draw a circle at the left eye position
        if(left_eye[0].y - left_eye[1].y) < 0.005:
            paglu.click()
            paglu.sleep(1)
    # display the processed frame
    cv2.imshow("camera feed <3", frame)

    cv2.waitKey(1) 
