"""

"h" {
    "media": {
        id: {
            title
            type
            percent_like
            percent_dislike
            percent_meh
            num_likes
            year
            image
        }
    }

    "relations": {
        media_id1: {
            media_id2: score
        }

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
ID = 3
LIKE = 4
TYPE = 5
P_LIKE = 6
P_DISLIKE = 7
P_MEH = 8
NUM_LIKES = 9
YEAR = 10
IMAGE = 11

def parse_csv():
    with open('data.csv', encoding="ISO-8859-1") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # assumes all users are grouped for easier reading
        user_rows = []
        user_row_ids = set()
        all_row_ids = set()
        stored_user = None
        first_row = True


        # TEMP
        count = 0

        for row in csv_reader:
            # skip first row
            if first_row:
                first_row = False
                continue

            # TEMP: count
            if count < 10:
                count += 1
            else:
                break

            # adds to media db
            if row[ID] not in all_row_ids:
                all_row_ids.add(row[ID])
                add_media_data(row)

            if stored_user is None:
                stored_user = row[USER]

            # prevents duplicates
            if row[USER] == stored_user and row[ID] not in user_row_ids:
                user_rows.append(row)
                user_row_ids.add(row[ID])
            else:
                add_relation_data(user_rows)
                stored_user = row[USER]
                user_rows.clear()
                user_row_ids.clear()

        # final user
        add_relation_data(user_rows)

def add_media_data(row):
    client = MongoClient()
    media_db = client.h["media"]
    data = {"_id": int(row[ID]), "title": row[TITLE]}
    media_db.insert(data)

def add_relation_data(rows):
    """
    goes through each row squared
    inserts all of row2 media into row1 as long as row2 != row1
    """
    client = MongoClient()
    relations_db = client.h["relations"]
    #for row1 in rows:
    #    for row2 in rows:
    #        if row1[ID] == row2[ID]:
    #            continue

    #        relations_db

    #print(list(row[TITLE] for row in rows))
    print(len(rows))

def main():
    client = MongoClient()
    #relations_db = client.h["relations"]
    media_db = client.h["media"]

    #sample_media = {"h": "h"}
    #media_db.insert_one(sample_media)
    #parse_csv()

    for media in media_db.find():
        pprint.pprint(media)
        print(type(media["_id"]))

    # deleting all
    #media_db.delete_many({})

if __name__ == "__main__":
    main()
    #parse_csv()

