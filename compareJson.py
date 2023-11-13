import json
import Levenshtein as lev
import numpy as np
from Levenshtein import ratio

def printJson(file_name):
    # Opening JSON file
    f = open(file_name)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    print("READING EXTRACT FROM PAGE#:"+data["pageNumber"])
    print("SCHEDULE NAME:"+data["scheduleName"])

    for scheduleInfo in data["schedules"]:
        scheduleinfo = json.loads(json.dumps(scheduleInfo))
        print(scheduleinfo["key"])
        print(scheduleinfo["value"])

    # Closing file
    f.close()

# print("EXTRACT FROM CURRENT FILE")
# printJson("CURR_JSON3.json")
# print("###############################################")
# print("EXTRACT FROM OLD FILE")
# printJson("OLD_JSON3.json")


def compareJson(file_name_curr,file_name_old):
    # Opening JSON file
    f = open(file_name_curr)
    data_curr = json.load(f)

    f1 = open(file_name_old)
    data_old = json.load(f1)
    lines = []
    for scheduleInfo in data_curr["schedules"]:
        scheduleinfo = json.loads(json.dumps(scheduleInfo))
        key_curr=scheduleinfo["key"]

        value_curr = scheduleinfo["value"]

        dist_arr=[]
        for scheduleInfo_old in data_old["schedules"]:
            scheduleinfo_old = json.loads(json.dumps(scheduleInfo_old))
            key_old = scheduleinfo_old["key"]

            dist_arr.append(ratio(key_curr, key_old))

        max_ind=np.argmax(dist_arr)
        max_ratio = np.max(dist_arr)

        if (max_ratio > 0.7):
            lines.append("IN CURRENT REPORT:\n")
            lines.append(key_curr+"\n")
            lines.append(value_curr+"\n")
            lines.append("IN OLD REPORT:\n")
            lines.append(data_old["schedules"][max_ind]["key"]+"\n")
            lines.append(data_old["schedules"][max_ind]["value"]+"\n")

        # Closing file
        f.close()
        f1.close()

    return lines


lines = compareJson("CURR_JSON1.json","OLD_JSON1.json")
with open('COMPARE_OUTPUT_1.txt', 'w') as f:
    for line in lines:
        f.write(line)

f.close()