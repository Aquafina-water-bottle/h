"""

"media": {
    id: {
        type
        p_like
        p_dislike
        p_meh
        num_like
        year
        image
    }
}

"relations": {
    "media_id1": {
        media_id2: score
    }

}
"""

import csv
import pprint

import pymongo
from pymongo import MongoClient

USER = 0
TITLE = 1
KEY = 2
NAME = 3
ID = 4
LIKE = 5
TYPE = 6
P_LIKE = 7
P_DISLIKE = 8
P_MEH = 9
NUM_LIKES = 10
YEAR = 11
IMAGE = 12

def parse_csv():
    with open('data.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        rows = list(csv_reader)

def add_data(rows):
    pass

def main():
    client = MongoClient()
    relations_db = client.h["relations"]
    media_db = client.h["media"]

    #sample_media = {"h": "h"}
    #media_db.insert_one(sample_media)

    # goes through each row squared
    # inserts all of row2 media into row1 as long as row2 != row1
    with open('data.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # assumes all users are grouped for easier reading
        user_rows = []
        stored_user = None
        for row in csv_reader:
            if stored_user is None:
                stored_user = row[USER]

            if row[USER] == stored_user:
                user_rows.append(row)
            else:
                add_data(user_rows)
                stored_user = row[USER]
                user_rows.clear()


    print("before")
    for media in media_db.find():
        pprint.pprint(media)

    # deleting all
    #db.delete_many({})

    print("after")
    for media in media_db.find():
        pprint.pprint(media)

if __name__ == "__main__":
    main()
    #parse_csv()

