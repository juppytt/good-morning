import csv
import os
import shutil
from datetime import datetime

### CSV file configuration
DB_SET = "time.csv"
fname_set = ['User Id', 'Time']

DB_REC = "rec.csv"
fname_rec = ['User Id', 'User Name', 'Record']

DB_BALANCE = "balance.csv"
fname_balance = ['User Id', 'Amount']

## ERROR CODE
ERROR_SKIPPED_BEFORE = -1
ERROR_SKIP_LATE = -2


### CSV database common functions
def init_db(db, fname):
    with open(db, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fname)
        writer.writeheader()

    db_copy = db+".copy"
    shutil.copy2(db, db_copy)



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
        print("Failed: Trying to change User Id")
        return -1

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
    db_copy = db+".copy"
    shutil.copy2(db, db_copy)

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

    db_copy = db+".copy"
    shutil.copy2(db, db_copy)

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
    db_copy = db+".copy"
    shutil.copy2(db, db_copy)

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
    db_copy = db+".copy"
    shutil.copy2(db, db_copy)


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
    res = res | rmv_db(DB_BALANCE, fname_balance, user_id)
    return res

### ADD USER
# update or create user info
def add_db_user(user_id, user_name=""):
    data = query_db(DB_REC, user_id)
    res = 0
    if (data == "" or data["User Name"] == ""):
        res = res |  add_db(DB_REC, fname_rec, {"User Id": user_id, "User Name": user_name, "Record": 0})

    data = query_db(DB_BALANCE, user_id)
    if (data == ""):
        res = res |  add_db(DB_BALANCE, fname_balance, {"User Id": user_id, "Amount": 10000})


    return res

def set_user_name_db(user_id, user_name):
    add_db_user(user_id, user_name)
    data = query_db(DB_REC, user_id)
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
# return 0 if time1 <= time2, else -1
def compare_time(time1, time2):
    (h1, m1) = time1.split(':')
    (h2, m2) = time2.split(':')
    if h1 < h2:
        return 0
    if h1 > h2:
        return -1
    if m1 <= m2:
        return 0
    return -1

def is_success(user_id, time):
    time_db = get_time_db(user_id)
    if (time_db) == "":
        print("Failed! Wake-up time not set")
        return -1
    return compare_time(time, time_db)

### RECORD WAKEUP TIME
def record_time_db(user_id, user_name):
    print("record_time_db")
    current = datetime.now()
    time = current.strftime("%H:%M")

    # record late!
    res = is_success(user_id, time)

    if (res >= 0):
        add_db_user(user_id, user_name)
        data = query_db(DB_REC, user_id)
        record = data["Record"]
        record = int(record)
        record = record | (1<<current.weekday())
        mod_db(DB_REC, user_id, fname_rec,
               {'User Id': user_id, 'User Name': user_name, 'Record' : record})

    return res, time

def record_skip_db(user_id, user_name):
    print("record_skip_db")
    current = datetime.now()
    time = current.strftime("%H:%M")
    if compare_time(time, "22:00") == 0:
        add_db_user(user_id, user_name)
        data = query_db(DB_REC, user_id)
        record = data["Record"]
        record = int(record)

        weekday = current.weekday()

        if weekday == 6:
            weekday = -1
        check_skip = record >> 5
        if check_skip > 0:
            return ERROR_SKIPPED_BEFORE
        else:
            record = record | (1<<(weekday+5+1))
            mod_db(DB_REC, user_id, fname_rec,
                   {'User Id': user_id, 'User Name': user_name, 'Record': record})
            return 0
    else:
        return ERROR_SKIP_LATE

def dump_record(data):
    text = "* Mon   Tue   Wed   Thr    Fri    Total*\n"
    count = 0
    score = int(data)
    weekday = datetime.now().weekday()

    skip = 0
    for i in range(5):
        if  i > weekday:
            if (score & (1<<(i+5))):
                text = text + "  :last_quarter_moon_with_face:  "
            else:
             text = text + "  :white_medium_square:  "
        else:
            if (score & (1<<i)):
                text = text + "  :sunny:  "
                count = count + 1
            elif (score & (1<<(i+5))):
                text = text + "  :last_quarter_moon_with_face:  "
                skip += 1
            else:
                text = text + "  :cloud:  "

    total_score = weekday+1
    total_score = total_score - skip
    text = text + ("  *%d/%d*" % (count, total_score))
    return text

def dump_balance(data):
    text = "*%s won*" % data
    return text

def extract_score(data, weekday):
    count = 0
    skip = False
    for i in range(5):
        if (data & (1<<i)):
            count = count + 1
    for i in range(5, 5+weekday+1):
        if (data & (1<<i)):
            skip = True
            break
    return count, skip

def get_record_db(user_id):
    print("get_record_db: " + user_id)
    data = query_db(DB_REC, user_id)
    if data is not "":
        data = data["Record"]
        return dump_record(data)

    else:
        return "Error: No such user?"

def get_balance_db(user_id):
    print("get_balance_db: " + user_id)
    data = query_db(DB_BALANCE, user_id)
    if data is not "":
        data = data["Amount"]
        return dump_balance(data)

    else:
        return "Error: No such user?"


skip_name = "Test Honja"

### Penalty & Weekly Report

def get_penalty():
    ll = dump_db(DB_REC, fname_rec)
    num = len(ll)
    total_penalty = 0
    weekday = datetime.now().weekday()
    total_score = weekday+1
    if weekday > 4:
        total_score = 5

    for i in range(len(ll)):
        if ll[i]['User Name'] == skip_name:
            del ll[i]
            break

    for i in range(len(ll)):
        rec = int(ll[i]['Record'])
        score, skip = extract_score(rec, weekday)
        ll[i]['Score'] = score
        total_score_user = total_score
        if skip:
            total_score_user = total_score_user - 1
        penalty = (score - total_score_user)*1000
        ll[i]['Penalty'] = penalty
        total_penalty = total_penalty - penalty

        # set user total score
        ll[i]['Total'] = total_score_user

    sort = sorted(ll, key = lambda i : i['Score'], reverse = True)
    top = sort[0]['Score']
    count = 0
    for  i in range(len(ll)):
        if sort[i]['Score'] == top:
            count = count+1
        else:
            break

    for i in range(count):
        sort[i]['Penalty'] = sort[i]['Penalty'] + (total_penalty/count)
    return sort


def get_weekly_db():

    weekday = datetime.now().weekday()
    total_score = weekday+1
    if weekday > 4:
        total_score = 5
    data = get_penalty()
    res = "*{:<18}".format("Name") + "Score      " + "Penalty*\n"
    for i in range(len(data)):
        name = data[i]['User Name']
        if name == "":
            name = "Unknown"
        res = res + "*{:<18}* ".format(name)
        res = res + str(data[i]['Score']) + ("/%d      " % data[i]['Total'])
        res = res + "*" + str(data[i]['Penalty']) + " won*\n"


    return res


def erase_record_db():
    set_db(DB_REC, fname_rec, "Record", 0)
    return 0

def update_penalty_db():
    print("update_penalty_db")
    res = ""
    data = get_penalty()
    for i in range(len(data)):
        balance_data = query_db(DB_BALANCE, data[i]['User Id'])
        if balance_data == "":
            print("Error! no user " + data[i]['User Id'])
            continue
        amount = int(balance_data['Amount'])
        amount = amount + data[i]['Penalty']
        new = balance_data
        new['Amount'] = amount
        mod_db(DB_BALANCE, data[i]['User Id'], fname_balance, new)

        if amount <= 0:
            if res == "":
                res = res + ":bank: *Alert from GoodMorning Bank*\n"

            text =  "*" + data[i]['User Name'] + "*, you've run out of balance: "
            text = text + "*" + str(amount) + "* won\n"
            res = res + text

    print("Update_penalty_db Success")
    return res


