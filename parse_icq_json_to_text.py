#!/usr/bin/python

import json
import os
import sys
import datetime


def parse(fname: str):
    history = []
    history = []
    users = {}
    with open(fname, 'r', encoding="utf-8") as f:
        raw_history = json.load(f)["results"]
    try:
        chat_name = raw_history["messages"][0]["chat"]["name"]
    except Exception as ex:
        print(fname, ex)
        return False

    for s in raw_history["persons"]:
        if "friendly" in s and "sn" in s:
            users.update({s["sn"]: s["friendly"]})
    for s in raw_history["messages"]:
        if "text" in s and "chat" in s and "time" in s:
            #            history.append({"sender": users[s["chat"]["sender"]],
            #                            "time": str(datetime.datetime.fromtimestamp(s["time"])),
            #                            "text": s["text"]})
            history.append(users[s["chat"]["sender"]]
                           + " (" + str(datetime.datetime.fromtimestamp(s["time"])) + "):"
                           + s["text"])
    print(chat_name + ": " + str(len(history)) + " messages")
    history.reverse()
    try:
        with open(chat_name.replace("/", "") + "_history.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(history))
    except Exception as ex:
        print(ex)
        with open(fname + "_history.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(history))
    return True


if __name__ == '__main__':
    parse(sys.argv[1])

