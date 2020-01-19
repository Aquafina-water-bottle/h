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


# actual start row is 0 with name specification
# so always skipped and starts at 2nd row, indexed 1
START_ROW = 1


# gets client, password lol
with open("password.txt") as file:
    _client_password = file.read().strip()
    CLIENT = MongoClient(_client_password)

MEDIA_DB = CLIENT.h["media"]
RELATIONS_DB = CLIENT.h["relations"]
GLOBAL_RELATIONS = {}

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
    # _id string
    data = {"_id": row[ID], "title": row[TITLE]}
    try:
        MEDIA_DB.insert(data)
    except pymongo.errors.DuplicateKeyError:
        pass

def add_relation_data(rows):
    """
    goes through each row squared
    inserts all of row2 media into row1 as long as row2 != row1

    NOTE: does NOT add to mongodb yet due to query delays
    just skips duplicate errors for now instead of updating
    """

    # stores row1 -> row2 -> score
    # might have to switch to query
    for row1 in rows:
        for row2 in rows:
            k1 = row1[ID]
            k2 = row2[ID]
            if k1 == k2:
                continue

            #data2 = {"_id": k2, "$inc": {"score": 1}}
            #RELATIONS_DB.find_one_and_update(data1, data2 upsert=True)
            try:
                RELATIONS_DB[k1].update_one(
                        {"_id": k2}, {"$inc": {"score": 1}}, upsert=True)
            except pymongo.errors.DuplicateKeyError:
                pass
            #result1.insert(data2)

            #if row1[ID] not in GLOBAL_RELATIONS:
            #    GLOBAL_RELATIONS[row1[ID]] = {}     # empty dict
            #if row2[ID] not in GLOBAL_RELATIONS[row1[ID]]:
            #    GLOBAL_RELATIONS[row1[ID]][row2[ID]] = 0
            #GLOBAL_RELATIONS[row1[ID]][row2[ID]] += 1

            #data = {"_id": row2[ID],
            #RELATIONS_DB[row1[ID]]

    for k1 in GLOBAL_RELATIONS:
        #data1 = {"_id": k1}
        #result1 = RELATIONS_DB.insert_one(data1)
        data2_list = [{"_id": k2, "score": GLOBAL_RELATIONS[k1][k2]}
                for k2 in GLOBAL_RELATIONS[k1]]

        try:
            RELATIONS_DB[k1].insert_many(data2_list)
        except pymongo.errors.BulkWriteError:
            pass

        #for k2 in GLOBAL_RELATIONS[k1]:
        #    data2 = {"_id": k2, "score": GLOBAL_RELATIONS[k1][k2]}
        #    #RELATIONS_DB.find_one_and_update(data1, data2 upsert=True)
        #    try:
        #        RELATIONS_DB[k1].insert(data2)
        #    except pymongo.errors.DuplicateKeyError:
        #        pass
        #    #result1.insert(data2)


    #print(list(row[TITLE] for row in rows))
    #print(len(rows))
    #pprint.pprint(GLOBAL_RELATIONS)

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

