import csv
import os
from datetime import datetime


### CSV file conf
DB_SET = "time.csv"
fname_set = ['User Id', 'Time']

DB_REC = "rec.csv"
fname_rec = ['User Id', 'User Name', 'Record']


### CSV database common functions
def init_db(db, fname):
    with open(db, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fname)
        writer.writeheader()

def query_db(db, user_id):
    if not os.path.exists(db):
        return ""

    with open(db, mode='r') as csv_file:
        for row in csv.DictReader(csv_file):
            if (row['User Id'] == user_id):
                return row

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
        init_db(db, fname)

    with open(db, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fname)
        print(data)
        writer.writerow(data)

    print("Success")
    return 0

def rmv_db(db, fname, user_id):
    print("rmv_db " + db + " " + user_id)
    if not os.path.exists(db):
        print("Failed: No DB")
        return -1

    db_tmp = db+".tmp"
    with open(db, mode='r') as inp, open(db_tmp, mode='w') as out:
        reader = csv.DictReader(inp, fieldnames = fname)
        writer = csv.DictWriter(out, fieldnames = fname)

        for row in reader:
            if (row['User Id'] == user_id):
                continue
            else:
                writer.writerow(row)

    os.rename(db_tmp, db)
    print("Success")
    return 0

def set_db(db, fname, key, data):
    print("set_db " + db)

    if not os.path.exists(db):
        print("Failed: No DB")
        return -1

    db_tmp = db+".tmp"
    with open(db, mode='r') as inp, open(db_tmp, mode='w') as out:
        reader = csv.DictReader(inp, fieldnames = fname)
        writer = csv.DictWriter(out, fieldnames = fname)

        header = True
        for row in reader:
            if header:
                header = False
                writer.writerow(row)
                continue
            row_data = row
            row_data[key] = data
            writer.writerow(row_data)

    os.rename(db_tmp, db)
    print("Success")
    return 0



def dump_db(db, fname):
    print("get_all_db " + db)
    if not os.path.exists(db):
        print("Failed: No DB")
        return -1

    res = []
    with open(db, mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames = fname)
        header = True
        for row in reader:
            if header:
                header = False
                continue
            res.append(row)
    return res

### REMOVE USER
def rmv_db_user(user_id):
    res = rmv_db(DB_SET, fname_set, user_id)
    res = res | rmv_db(DB_REC, fname_rec, user_id)
    return res

### ADD USER
def add_db_user(user_id):
    return add_db(DB_REC, fname_rec, {"User Id": user_id, "User Name": "", "Record": 0})

def set_user_name_db(user_id, user_name):
    data = query_db(DB_REC, user_id)
    if (data == ""):
        print("Failed! No user " + user_id)
        return -1
    if (data["User Name"] != user_name):
        data["User Name"] = user_name
        mod_db(DB_REC, user_id, fname_rec, data)
    return 0


### SET DB
def set_time_db(user_id, time):
    print("set_time_db")

    if time == "" or user_id == "":
        print("Invlaid input")
        return -1


    if not os.path.exists(DB_SET):
        init_db(DB_SET, fname_set)

    data = query_db(DB_SET, user_id)

    # has previously stored data
    if data is not "":
        db_time = data["Time"]
        # nothing to update
        if db_time == time:
            return 0

        # update time
        return mod_db(DB_SET, user_id, fname_set, {'User Id': user_id, 'Time' : time})

    # add data
    return add_db(DB_SET, fname_set, {'User Id': user_id, 'Time' : time})


def get_time_db(user_id):
    print("get_time_db")
    data = query_db(DB_SET, user_id)
    if data is not "":
        data = data["Time"]
    return data

### CHECK USER SUCCESS
def is_success(user_id, time):
    time_db = get_time_db(user_id)
    if (time_db) == "":
        print("Failed! Wake-up time not set")
        return -1
    (h, m) = time.split(':')
    (h_db, m_db) = time_db.split(':')
    if h < h_db:
        return 0
    if h > h_db:
        return -1
    if m <= m_db:
        return 0
    return -1

### RECORD WAKEUP TIME
def record_time_db(user_id, user_name):
    print("record_time_db")
    current = datetime.now()
    time = current.strftime("%H:%M")

    # record late!
    res = is_success(user_id, time)

    if (res >= 0):
        record = query_db(DB_REC, user_id)["Record"]
        record = int(record)
        record = record | (1<<current.weekday())
        mod_db(DB_REC, user_id, fname_rec,
               {'User Id': user_id, 'User Name': user_name, 'Record' : record})

    return res, time

def dump_record(data):
    text = "*Mon  Tue  Wed   Thr   Fri   Total*\n"
    count = 0
    score = int(data)
    for i in range(5):
        if (score & (1<<i)):
            text = text + "    1   "
            count = count + 1
        else:
            text = text + "    0   "

    text = text + (" *%d/5*" % count)
    return text
def extract_score(data):
    count = 0
    for i in range(5):
        if (data & (1<<i)):
            count = count + 1
    return count

def get_record_db(user_id):
    print("get_record_db: " + user_id)
    data = query_db(DB_REC, user_id)
    if data is not "":
        data = data["Record"]
        return dump_record(data)

    else:
        return "Error: No such user?"


### WEEKLY REPORT
def get_weekly_db():
    ll = dump_db(DB_REC, fname_rec)
    num = len(ll)
    total = 0
    for i in range(len(ll)):
        rec = int(ll[i]['Record'])
        score = extract_score(rec)
        ll[i]['Score'] = score
        penalty = (score - 5)*1000
        ll[i]['Penalty'] = penalty
        total = total - penalty

    sort = sorted(ll, key = lambda i : i['Record'], reverse = True)

    print(sort)

    top = sort[0]['Record']
    count = 0
    for  i in range(len(ll)):
        if sort[i]['Record'] == top:
            count = count+1
        else:
            break

    for i in range(count):
        sort[i]['Penalty'] = sort[i]['Penalty'] + (total/count)

    res = "*{:<18}".format("Name") + "Score      " + "Penalty*\n"
    for i in range(len(ll)):
        name = sort[i]['User Name']
        if name == "":
            name = "Unknown"
        res = res + "*{:<18}* ".format(name)
        res = res + str(sort[i]['Score']) + "/5      "
        res = res + "*" + str(sort[i]['Penalty']) + " won*\n"

    return res


def erase_record_db():
    set_db(DB_REC, fname_rec, "Record", 0)
    return 0


