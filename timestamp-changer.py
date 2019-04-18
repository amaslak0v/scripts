import os
import time
import datetime
import sys

"""
Changes timestamp for all photos in directory.
Sorts photos by name and add's 1min interval for each.
"""

class Timestamp():

    def __init__(self, day, month, year):
        self.year = year
        self.month = month
        self.day = day
        self.hour = datetime.datetime.now().hour
        self.minute = datetime.datetime.now().minute
        self.second = datetime.datetime.now().second

    def __repr__(self):
        return '{}-{}-{} {}:{}:{}'.format(
                    self.year,
                    self.month,
                    self.day,
                    self.hour,
                    self.minute,
                    self.second)


class TimestampChanger():

    def get_sorted_photos_list(self, entries):
        photos = {}
        for entry in entries:
            photos[int(entry.name.strip('.JPG'))] = entry
        return dict(sorted(photos.items())).values()

    def change_timestamp(self, dir_name, date):
        with os.scandir(dir_name) as entries:
            for entry in self.get_sorted_photos_list(entries):
                # Add 1 min to photo
                date = date + datetime.timedelta(seconds=60)
                self.modify_photo(entry, date)

    def modify_photo(self, entry, timestamp):
        modTime = time.mktime(timestamp.timetuple())
        os.utime(entry, (modTime, modTime))

def main(dir_name, date):
    # Example: modify_date.py photos/ 17-4-2018
    #todo Add %H:%M:%S 
    timestamp = Timestamp(*date.split('-'))
    changer = TimestampChanger()
    print("=> Changing timestamp in {}".format(dir_name))
    print("=> Timestamp: {}".format(date))

    changer.change_timestamp(dir_name,
        datetime.datetime.strptime(repr(timestamp, '%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
