import cv2
from multiprocessing import Process, Queue
import time

class Main:
    defaultVideo = "vid2.mp4"
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
            print("loop")
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
            cap = cv2.VideoCapture("videos/" + videoPath)
            while True:
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("Player", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        stopped = True
                        break
                else:
                    #cap.release()
                    break
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
                if bbox is not None:
                    q.put(data)
            cv2.waitKey(20)

if __name__ == "__main__":
    main = Main()
    main.run()