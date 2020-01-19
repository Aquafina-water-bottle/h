"""

"h" {
    "media": {
        _id (str): {
            title:
            type:
            percent_like:
            percent_dislike:
            percent_meh:
            num_likes:
            year:
            image:
        }
    }

    "relations": {
        media_id1: {
            _id (str):
            data: {
                _id:
                score:
            }
        }

    }
}

"""

import re
import csv
import pprint
from collections import deque

import pymongo
from pymongo import MongoClient, InsertOne, UpdateOne
from pymongo.errors import BulkWriteError

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


# actual start row is 0 with name specification
# so always skipped and starts at 2nd row, indexed 1
START_ROW = 1

MAX_BATCH_SIZE = 10000000


# gets client, password lol
# with open("password.txt") as file:
#     _client_password = file.read().strip()
#     CLIENT = MongoClient(_client_password)
CLIENT = MongoClient()

MEDIA_DB = CLIENT.h["media"]
RELATIONS_DB = CLIENT.h["relations"]

MEDIA_COLLECTION_INSERTS = deque()


def parse_csv():
    with open('data.csv', encoding="ISO-8859-1") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # assumes all users are grouped for easier reading
        user_rows = []
        user_row_ids = set()
        all_row_ids = set()
        stored_user = None

        count = -1

        for row in csv_reader:
            count += 1

            # skips all rows until START_ROW
            if count <= START_ROW:
                continue

            if (count % 10) == 0:
                print(str(count) + "...")

            # adds to media db
            if row[ID] not in all_row_ids:
                all_row_ids.add(row[ID])
                add_media_data(row)

                if len(MEDIA_COLLECTION_INSERTS) > MAX_BATCH_SIZE:
                    write_media_data()
                    MEDIA_COLLECTION_INSERTS.clear()

            if stored_user is None:
                stored_user = row[USER]

            # prevents duplicates
            if row[USER] == stored_user and row[ID] not in user_row_ids:
                user_rows.append(row)
                user_row_ids.add(row[ID])
            else:
                add_and_write_relation_data(user_rows)
                stored_user = row[USER]
                user_rows.clear()
                user_row_ids.clear()

        # final user
        add_and_write_relation_data(user_rows)

        write_media_data()


def add_media_data(row):
    # _id string
<<<<<<< HEAD
    data = {"_id": row[ID], "type": row[TYPE],
            "title": row[TITLE], "image": row[IMAGE]}
=======
    data = {"_id": row[ID], "type": row[TYPE], "title": row[TITLE], "image": row[IMAGE]}
>>>>>>> f4588ab40ee13206011a2b92e433e1e1f4ec7d80
    MEDIA_COLLECTION_INSERTS.append(data)


def write_media_data():
<<<<<<< HEAD
    MEDIA_DB.insert_many(MEDIA_COLLECTION_INSERTS, ordered=False)
=======
    try:
        MEDIA_DB.insert_many(MEDIA_COLLECTION_INSERTS, ordered=False)
    except BulkWriteError as bwe:
        pprint.pprint(bwe.details)
>>>>>>> f4588ab40ee13206011a2b92e433e1e1f4ec7d80


def add_and_write_relation_data(rows):
    """
    goes through each row squared
    inserts all of row2 media into row1 as long as row2 != row1

    NOTE: does NOT add to mongodb yet due to query delays
    just skips duplicate errors for now instead of updating
    """

    # stores row1 -> row2 -> score
    # might have to switch to query

    batch = deque()

    for row1 in rows:

        k1 = row1[ID]
<<<<<<< HEAD
        batch = deque()
=======
>>>>>>> f4588ab40ee13206011a2b92e433e1e1f4ec7d80

        for row2 in rows:
            k2 = row2[ID]
            if k1 == k2:
                continue

<<<<<<< HEAD
            batch.append(UpdateOne({"_id": k2}, {"$inc": {"score": 1}},
                                   upsert=True))

        try:
            RELATIONS_DB[k1].bulk_write(batch, ordered=False)
        except BulkWriteError as bwe:
            pprint.pprint(bwe.details)
=======
            batch.append(UpdateOne({"from": k1, "to": k2}, {"$inc": {"score": 1}}, upsert=True))

            if len(batch) > MAX_BATCH_SIZE:
                try:
                    RELATIONS_DB.bulk_write(list(batch), ordered=False)
                except BulkWriteError as bwe:
                    pprint.pprint(bwe.details)
                batch.clear()

    try:
        RELATIONS_DB.bulk_write(list(batch), ordered=False)
    except BulkWriteError as bwe:
        pprint.pprint(bwe.details)

>>>>>>> f4588ab40ee13206011a2b92e433e1e1f4ec7d80


def main():

    #sample_media = {"h": "h"}
    #MEDIA_DB.insert_one(sample_media)
    #parse_csv()

    for media in MEDIA_DB.find():
        pprint.pprint(media)
        print(type(media["_id"]))

    # deleting all
    #MEDIA_DB.delete_many({})


def delete_all():
    MEDIA_DB.delete_many({})
    RELATIONS_DB.delete_many({})

    rx_RELATIONS = re.compile(r'relations\.\d+')
    for col_name in CLIENT.h.collection_names():
        if rx_RELATIONS.match(col_name):
            print(col_name)
            CLIENT.h[col_name].drop()

if __name__ == "__main__":
    #main()
    #delete_all()
    parse_csv()

