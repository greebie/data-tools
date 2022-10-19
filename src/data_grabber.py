from urllib.error import HTTPError
import urllib.request as request
import datetime
import os
import logging

INTERVAL_DAY = "D"
INTERVAL_MONTH = "M"
INTERVAL_YEAR = "Y"

class MonthlyState:
    grabber = None

    def __init__(self, grabber):
        grabber = grabber

    def build(self):
        if self.grabber == None:
            raise Exception("No grabber called for state class")
        end = self.grabber.endtime
        start = self.grabber.starttime
        datelist = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
        try:
            self.grabber.createDir(str(start.year))
        except FileExistsError as fe:
            logging.warning(f"Directory for {str(start.year)} already exists")
            logging.warning(f"Via error: fe")
        curr_year = start.year
        for n in datelist:
            source = self.grabber.url + \
              "/" + str(n.year) + "/" + str(n.month) + "/" + str(n.day) + "/" +\
              self.grabber.filename
            destination = self.grabber.home + \
              "/" + str(n.year) + "/" + str(n.month) + "/" + str(n.day) + "/" + \
              self.grabber.filename
            if n.year > curr_year:
                self.grabber.createDir(grabber.home + str(n.year))
                curr_year = n.year



class DailyState:
    grabber = None

    def __init__(self, grabber):
        self.grabber = grabber

    def build(self):
        if self.grabber == None:
            raise Exception("No grabber called for state class")
        end = self.grabber.endtime
        start = self.grabber.starttime
        datelist = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
        try:
            self.grabber.createDir(str(start.year))
            self.grabber.createDir(str(start.year) + '/' + str(start.month))
        except FileExistsError as fe:
            logging.warning(f"Directory for {str(start.year)} already exists")
            logging.warning(f"Via error: fe")
            
        curr_year = start.year
        curr_month = start.month
        for n in datelist:
            source = self.grabber.url + \
              "/" + str(n.year) + "/" + str(n.month) + "/" + str(n.day) + "/" +\
              self.grabber.filename
            destination = self.grabber.home + \
              "/" + str(n.year) + "/" + str(n.month) + "/" + str(n.day) + "/" + \
              self.grabber.filename
            if n.year > curr_year:
                self.grabber.createDir(grabber.home + str(n.year))
                curr_year = n.year
            if n.month > curr_month % 12:
                self.grabber.createDir(grabber.home + str(n.year) + "/" + str(n.month))
                curr_month = n.month
            self.grabber.createDir(grabber.home + str(n.year) + "/" + str(n.month) + "/" + str(n.day))
            self.grabber.getData(source, destination)


class YearlyState:

    grabber = None

    def __init__(self, grabber):
        grabber = grabber

    def build(self):
        pass


class DataGrabber:
    grabState = None
    starttime = None
    endtime = None
    url = None
    filename = None
    home = "./"

    def __init__(self, url, starttime, endtime=datetime.datetime.now(), filename="data.json", interval=INTERVAL_DAY, home="./"):
        if home == "/":
            raise PermissionError("Do not use the root directory as home.")
        self.home = home
        self.url = url
        self.starttime = starttime
        self.endtime = endtime
        self.filename = filename
        if interval == INTERVAL_MONTH:
            self.changeState(MonthlyState(self))
        elif interval == INTERVAL_YEAR:
            self.changeState(YearlyState(self))
        else:
            self.changeState(DailyState(self))


    def getData(self, source, destination="./"):
        try:
            request.urlretrieve(source, destination)
        except HTTPError as httpe:
            logging.warning(f'Received an "{httpe}" error when trying to retrieve')
            logging.warning(f'the data from {source}')


    def changeState(self, newGrabState):
        self.grabState = newGrabState

    def createDir(self, path=""):
        try:
            os.mkdir(path)
        except FileExistsError as fe:
            print(fe)

    def build(self):
        self.grabState.build()


if __name__ == "__main__":
    print ("Provide the base url to grab the data")
    url = input()
    print("What is the startdate in YYYY-MM-DD format?")
    start = datetime.datetime.strptime(input(), "%Y-%m-%d")
    print("What is the end date in YYYY-MM-DD format? (CR if you want to use now.)")
    end = datetime.datetime.strptime(input(), "%Y-%m-%d")
    print("What time interval would you prefer? (Y/M/D)")
    interval = input()
    print("What filename does the api use?")
    fn = input()
    grabber = DataGrabber(url, start, end, fn)
    grabber.build()
    

