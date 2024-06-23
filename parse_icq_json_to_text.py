#!/usr/bin/python

import json
import os
import datetime


def parse(fname: str, chatinfo: str):
    history = []
    users = {}

    with open(chatinfo, 'r', encoding="utf-8") as f:
        try:
            user_info = json.load(f)
            for s in user_info["results"]["members"]:
                if "friendly" in s and "sn" in s:
                    users.update({s["sn"]: s["friendly"]})
        except Exception as ex:
            print("error while parsing " + chatinfo, ex)

    with open(fname, 'r', encoding="utf-8") as f:
        raw_history = json.load(f)
        print(raw_history)

    for s in raw_history:
        if "text" in s and "chat" in s and "time" in s:
            #            history.append({"sender": users[s["chat"]["sender"]],
            #                            "time": str(datetime.datetime.fromtimestamp(s["time"])),
            #                            "text": s["text"]})
            if s["chat"]["sender"] in users:
                sender = users[s["chat"]["sender"]]
            else:
                sender = s["chat"]["sender"]
            time = str(datetime.datetime.fromtimestamp(s["time"]))
            text = s["text"]
            history.append(sender + " (" + time + "):" + text)
    history.reverse()
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
        parsed_text = []
        for json_part in jsons:
            f = os.path.join("results", chat, "json", json_part)
            p = parse(f, chatinfo)
            parsed_text.extend(p)
        with open(os.path.join("parsed_results", chat + "_history.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(parsed_text))
