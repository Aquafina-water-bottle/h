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


# gets client, password lol
with open("password.txt") as file:
    _client_password = file.read().strip()
    CLIENT = MongoClient(_client_password)

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

        count_media = 0
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
                if count_media >= 20:
                    write_media_data()
                    count_media = 0
                    MEDIA_COLLECTION_INSERTS.clear()
                else:
                    all_row_ids.add(row[ID])
                    add_media_data(row)
                    count_media += 1

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

        if count_media > 0:
            write_media_data()


def add_media_data(row):
    # _id string
    data = {"_id": row[ID], "type": row[TYPE], "title": row[TITLE], "image": row[IMAGE]}
    MEDIA_COLLECTION_INSERTS.append(data)


def write_media_data():
    try:
        MEDIA_DB.insert_many(MEDIA_COLLECTION_INSERTS, ordered=False)
    except BulkWriteError as bwe:
        pprint.pprint(bwe.details)


def add_and_write_relation_data(rows):
    """
    goes through each row squared
    inserts all of row2 media into row1 as long as row2 != row1

    NOTE: does NOT add to mongodb yet due to query delays
    just skips duplicate errors for now instead of updating
    """

    # stores row1 -> row2 -> score
    # might have to switch to query
    for row1 in rows:

        k1 = row1[ID]
        batch = deque()

        for row2 in rows:
            k2 = row2[ID]
            if k1 == k2:
                continue

            # batch.append(UpdateOne({"_id": k2}, {"$inc": {"score": 1}}, upsert=True))
            batch.append(UpdateOne({"from": k1, "to": k2}, {"$inc": {"score": 1}}, upsert=True))

        try:
            RELATIONS_DB.bulk_write(list(batch), ordered=False)
        except BulkWriteError as bwe:
            pprint.pprint(bwe.details)


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

