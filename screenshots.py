from mss import mss
import datetime
import os
import settings
import pickle
import zlib
import time


class Screenshot:
    def __init__(self, username=None):
        self.mss = mss()
        self.mss.compression_level = 6
        self.file = None
        self.timestamp = datetime.timedelta(seconds=10)
        self.last_date = datetime.datetime.now()
        self.lock = True
        self.filename = None
        self.username = username

    def make_screens(self):
        screens = []

        for num, monitor in enumerate(self.mss.monitors[1:], 1):
            sct_img = self.mss.grab(monitor)

            screens.append({
                "username": self.username,
                "monitor": num,
                "size": sct_img.size,
                "bgra": zlib.compress(sct_img.rgb, 6),
                "name": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            })

        return screens

    def save(self, data):

        if self.last_date + self.timestamp < datetime.datetime.now():
            date = datetime.datetime.now()
            self.file.close()
            self.filename = date.strftime("%Y%m%d%H%M%S")
            self.file = open(
                os.path.join(settings.BASE_DIR, f"screenshots/"
                                                f"{self.filename}"),
                "ba+"
            )
            self.last_date = date

        if not self.file:
            self.filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.file = open(os.path.join(settings.BASE_DIR,
                                          f'screenshots/{self.filename}'),
                             "ba+")

        pickle.dump(data, self.file)
        self.file.flush()

    def run_infinitive(self, sleep_between_shots=0.5):
        while True:
            scrs = self.make_screens()
            for s in scrs:
                self.save(s)
            time.sleep(sleep_between_shots)
