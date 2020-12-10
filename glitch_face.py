import cv2
import logging as log
import datetime as dt
from time import sleep
import numpy as np
import click

@click.command()
@click.option("-b", default = 10, help="blocks: number of NxN blocks to break up the image [0-50]")
@click.option("-o", default = 15, help="offset: offset glitch")
@click.option("-s", default = 50, help="value to scale width and height of area anonymized")
def main(b, o, s):
    #cascPath = "haarcascade_frontalface_default.xml"
    #face_cascade = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + './haarcascade_frontalface_default.xml')
    #faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + './haarcascade_frontalface_default.xml')
    #faceCascade = cv2.CascadeClassifier(cascPath)
    log.basicConfig(filename='webcam.log',level=log.INFO)
    
    video_capture = cv2.VideoCapture(0)
    anterior = 0
    
    def anonymize_face_pixelate(image, blocks=10):
        """
        use NxN blocks to break up image
        credit for this function goes to pyimage
        """
        (h, w) = image.shape[:2]
        xSteps = np.linspace(0, w, blocks + 1, dtype="int")
        ySteps = np.linspace(0, h, blocks + 1, dtype="int")
        for i in range(1, len(ySteps)):
            for j in range(1, len(xSteps)):
                startX = xSteps[j - 1]
                startY = ySteps[i - 1]
                endX = xSteps[j]
                endY = ySteps[i]
                roi = image[startY:endY, startX:endX]
                (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
                cv2.rectangle(image, (startX, startY), (endX, endY),(B, G, R), -1)
        return image


    def anonymize_face_gliitch(image, offset = 15):
        """
        offset right/left randomly
        inspired by the glitch_this library
        """
        (h, w) = image.shape[:2]
        if h < 1:
            print("nooooo: " + str(h))
        else:
            print(str(h))

        start_y = int(np.random.randint(0, h, size = 1))
        print("start_y")
        chunk_height = np.random.randint(1, int(h/4))
        print("chunk_height")
        chunk_height = min(chunk_height, h - start_y)
        print("chunk_height")
        stop_y = int(start_y + chunk_height)
        print("stop_y")
        switcher = np.random.choice([True,False])
        if switcher == True:
            start_x = offset
            stop_x = h - start_x
            left_chunk = image[start_y:stop_y, start_x:]
            wrap_chunk = image[start_y:stop_y, :start_x]
            image[start_y:stop_y, :stop_x] = left_chunk
            image[start_y:stop_y, stop_x:] = wrap_chunk
        else:
            stop_x = w - offset
            start_x = offset
            right_chunk = image[start_y:stop_y, :stop_x]
            wrap_chunk = image[start_y:stop_y, stop_x:]
            image[start_y:stop_y, start_x:] = right_chunk
            image[start_y:stop_y, :start_x] = wrap_chunk
        return image
    
    def anonymize_face_row_color(image, offset = 15, odds_true_color = 5):
        """
        random row chunks of color
        """
        (h, w) = image.shape[:2]
        start_y = int(np.random.randint(0, h, size = 1))
        chunk_height = np.random.randint(1, int(h/20))
        chunk_height = min(chunk_height, h - start_y)
        stop_y = int(start_y + chunk_height)
        choice_range = np.linspace(start=0,
                stop=odds_true_color-1,
                num=odds_true_color).astype(int)
        diffr = np.random.randint(low = 0, high = 255, size=1)
        switcher = np.abs(np.random.choice(a = choice_range))
        start_x = offset
        stop_x = w-offset
        roi = image[start_y:stop_y, start_x:stop_x]
        if switcher == 0:
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0]),
            np.abs(cv2.mean(roi)[1]),
            np.abs(cv2.mean(roi)[2] - diffr),
            )]
        elif switcher == 1: 
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0]),
            np.abs(cv2.mean(roi)[1] - diffr),
            np.abs(cv2.mean(roi)[2]),
            )]
        elif switcher == 2: 
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0]),
            np.abs(cv2.mean(roi)[1] - diffr),
            np.abs(cv2.mean(roi)[2] - diffr),
            )]
        elif switcher == 3: 
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0] - diffr),
            np.abs(cv2.mean(roi)[1]),
            np.abs(cv2.mean(roi)[2] - diffr),
            )]
        elif switcher == 2: 
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0] - diffr),
            np.abs(cv2.mean(roi)[1]),
            np.abs(cv2.mean(roi)[2]),
            )]
        else:
            (B, G, R) = [int(x) for x in (
            np.abs(cv2.mean(roi)[0]),
            np.abs(cv2.mean(roi)[1]),
            np.abs(cv2.mean(roi)[2]),
            )]
    
        cv2.rectangle(image, (start_x, start_y), (stop_x, stop_y),(B, G, R), -1)
        return image
    
    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(2)
            pass
    
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
    
    
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            x, y, w, h = x-int(s/2), y-int(s/2), w+s, h+s
            sub_face = frame[y:y+h, x:x+w]
            sub_face = anonymize_face_pixelate(sub_face, blocks=b)
            sub_face = anonymize_face_gliitch(sub_face, offset=o)
            sub_face = anonymize_face_row_color(sub_face, offset=o, odds_true_color=6)
            frame[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
    
        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
    
    
        # Display the resulting frame
        cv2.imshow('Video', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        # Display the resulting frame
        cv2.imshow('Video', frame)
    
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
