import cv2
from multiprocessing import Process, Queue

class Main:
    defaultVideo = "vid.mkv"
    def __init__(self):
        self.__name = "Main"

    def run(self):
        # Start QR Scanner
        qrScanner = QRScanner()
        QrQue = Queue()
        qrScannerProcess = Process(target=qrScanner.scan, args=(QrQue,))
        qrScannerProcess.start()

        # Start Video Player
        self.showWindow()
        videoQue = Queue()
        videoProcess = Process(target=self.playVideo, args=(videoQue,))
        videoProcess.start()
        # Wait for QR Scanner to find QR Code
        while True:
            if not QrQue.empty():
                videoQue.put(QrQue.get())
            else:
                pass

    def showWindow(self):
        cv2.namedWindow("Player", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Player", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def playVideo(self, q, videoPath=defaultVideo):
        cap = cv2.VideoCapture("videos/" + videoPath)
        while True:
            ret, frame = cap.read()
            if not q.empty():
                videoPath = q.get()
                cap = cv2.VideoCapture("videos/" + videoPath)
            if ret:
                cv2.imshow("Player", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()

class QRScanner:
    def __init__(self):
        self.__name = "QRScanner"

    def scan(self, q):
        cam = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cam.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if bbox is not None:
                for i in range(len(bbox)):
                    cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 255), thickness=2)
                if data:
                    print("[+] QR Code detected, data:", data)
                    q.put(data)
            cv2.imshow("img", img)
            if cv2.waitKey(1) == ord("q"):
                break


if __name__ == "__main__":
    main = Main()
    main.run()