import cv2
from multiprocessing import Process, Queue
import time
from ffpyplayer.player import MediaPlayer

class Main:
    defaultVideo = "vid3"
    def __init__(self):
        self.__name = "Main"

    def run(self):
        # Start QR Scanner
        qrScanner = QRScanner()
        QrQue = Queue()
        qrScannerProcess = Process(target=qrScanner.scan, args=(QrQue,))
        qrScannerProcess.start()

        # Start Video Player
        #self.showWindow()
        videoQue = Queue()
        videoProcess = Process(target=self.playVideo, args=(videoQue,))
        videoProcess.start()
        # Wait for QR Scanner to find QR Code
        while True:
            if not QrQue.empty():
                print("code found")
                videoQue.put(QrQue.get())
            else:
                pass

    def playVideo(self, q, videoPath=defaultVideo):
        cv2.namedWindow("Player", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Player", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        stopped = False
        while not stopped:
            if not q.empty():
                videoPath = q.get()
            cap = cv2.VideoCapture("videos/" + videoPath + ".mp4")
            player = MediaPlayer("videos/" + videoPath + ".mp4")

            while True:
                ret, frame = cap.read()
                audio_frame, val = player.get_frame()

                if ret:
                    cv2.imshow("Player", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        stopped = True
                        break
                else:
                    #cap.release()
                    break
                if not q.empty():
                    break
                
                if val != 'eof' and audio_frame is not None:
                    #audio
                    img, t = audio_frame

                cv2.waitKey(20)

class QRScanner:
    def __init__(self):
        self.__name = "QRScanner"

    def scan(self, q):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            ret, frame = cap.read()
            if ret:
                data, bbox, _ = detector.detectAndDecode(frame)
                if bbox is not None and data != "":
                    q.put(data)
                    time.sleep(3)
            cv2.waitKey(20)

if __name__ == "__main__":
    main = Main()
    main.run()