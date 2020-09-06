import csv
import os

DB_SET = "time.csv"
fname_set = ['User Id', 'Time']


### CSV database common functions
def query_db(db, user_id):
    if not os.path.exists(db):
        return ""

    with open(db, mode='r') as csv_file:
        for row in csv.DictReader(csv_file):
            if (row['User Id'] == user_id):
                return row['Time']

        return ""

def mod_db(db, user_id, fname, data):
    print("mod_db")
    if not os.path.exists(db):
        print ("Failed: No DB")
        return -1

    if data['User Id'] != user_id:
        print("Failed: User Id")

    db_tmp = db+".tmp"
    with open(db, mode='r') as inp, open(db_tmp, mode='w') as out:
        reader = csv.DictReader(inp, fieldnames = fname)
        writer = csv.DictWriter(out, fieldnames = fname)

        for row in reader:
            if (row['User Id'] == user_id):
                print(data)
                writer.writerow(data)
            else:
                writer.writerow(row)

    os.rename(db_tmp, db)
    print("Success")
    return 0


def add_db(db, fname, data):
    print("add_db")
    if not os.path.exists(db):
        print("Failed: No DB")
        return -1

    with open(db, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fname)
        print(data)
        writer.writerow(data)

    print("Success")
    return 0


### Setting DB
def init_db_set():
    with open(DB_SET, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fname_set)
        writer.writeheader()

def set_time_db(user_id, time):
    print("set_time_db")

    if time == "" or user_id == "":
        print("Invlaid input")
        return -1


    if not os.path.exists(DB_SET):
        init_db_set()

    db_time = query_db(DB_SET, user_id)

    # has previously stored data
    if db_time is not "":

        # nothing to update
        if db_time == time:
            return 0

        # update time
        return mod_db(DB_SET, user_id, fname_set, {'User Id': user_id, 'Time' : time})

    # add data

    return add_db(DB_SET, fname_set, {'User Id': user_id, 'Time' : time})


def get_time_db(user_id):
    print("get_time_db")
    return query_db(DB_SET, user_id)


