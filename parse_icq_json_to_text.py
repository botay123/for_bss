#!/usr/bin/python

import json
import os
import datetime


def parse(fname: str, chatinfo: str):
    history = {}
    users = {}

    with open(chatinfo, 'r', encoding="utf-8") as f:
        try:
            user_info = json.load(f)
            if "members" in user_info["results"]:
                for s in user_info["results"]["members"]:
                    if "friendly" in s and "sn" in s:
                        users.update({s["sn"]: s["friendly"]})
        except Exception as ex:
            print("error while parsing " + chatinfo, ex, user_info)

    with open(fname, 'r', encoding="utf-8") as f:
        raw_history = json.load(f)

    for s in raw_history:
        if "text" in s and "time" in s:
            #            history.append({"sender": users[s["chat"]["sender"]],
            #                            "time": str(datetime.datetime.fromtimestamp(s["time"])),
            #                            "text": s["text"]})
            if "chat" in s:
                if s["chat"]["sender"] in users:
                    sender = users[s["chat"]["sender"]]
                else:
                    sender = s["chat"]["sender"]
            else:
                sender = "-"
            time = str(datetime.datetime.fromtimestamp(s["time"]))
            text = s["text"]
            history.update({s["time"]: sender + " (" + time + "):" + text})
#    try:
#        with open(chat_name.replace("/", "") + "_history.txt", "w", encoding="utf-8") as f:
#            f.write("\n".join(history))
#    except Exception as ex:
#        print(ex)
#        with open(fname + "_history.txt", "w", encoding="utf-8") as f:
#            f.write("\n".join(history))
    return history


if __name__ == '__main__':
    results = os.listdir("results")

    if not os.path.exists("parsed_results"):
        os.mkdir("parsed_results")

    for chat in results:
        jsons = os.listdir(os.path.join("results", chat, "json"))
        chatinfo = os.path.join("results", chat, "chatInfo.json")
        parsed_dict = {}

        for json_part in jsons:
            f = os.path.join("results", chat, "json", json_part)
            parsed_dict.update(parse(f, chatinfo))

        timestamps = parsed_dict.keys()
        timestamps = list(timestamps)
        timestamps.sort()

        with open(os.path.join("parsed_results", chat + "_history.txt"), "w", encoding="utf-8") as f:
            for t in timestamps:
                f.write("\n" + parsed_dict[t])
