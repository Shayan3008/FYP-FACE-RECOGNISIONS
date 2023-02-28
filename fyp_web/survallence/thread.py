import threading


class ModelThread(threading.Thread):

    def __init__(self, cameraId):
        self.cameraId = cameraId
        threading.Thread.__init__(self=self)
    
    # def run(self) -> None:
        
    