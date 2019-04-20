#coding:utf-8
import json
import csv
import glob

class Res:
    def __init__(self, line):
        # Basis 
        try:
            self.id = line["id"]
        except AttributeError:
            self.id = None
        
        try:
            self.map = line["map"]["splatnet"]
        except TypeError:
            self.map = None
        self.result = line["result"]
        self.version = line["game_version"]
        self.time = line["end_at"]["time"] - line["start_at"]["time"]
        
        # Standard / Private / Squad2, 4
        self.type = line["lobby"]["key"]

        if self.type == "standard":
            # Gachi / Regular
            self.mode = line["mode"]["key"]
            
            # Ranked Battle
            if self.mode == "gachi":
                self.rule = line["rule"]["name"]["en_US"]
                self.udemae = line["rank"]["key"]
                self.knockout = line["knock_out"]
                self.ocount = line["his_team_count"]
                self.mcount = line["my_team_count"]
                if self.udemae == "x":
                    self.egp = line["estimate_x_power"]
                else:
                    self.egp = line["estimate_gachi_power"]
            # Turf War
            else:
                self.mode = line["mode"]["key"]
        else:
            self.rule = line["rule"]["name"]["en_US"]
            self.mode = line["mode"]["key"]
            self.ocount = line["his_team_count"]
            self.mcount = line["my_team_count"]
            self.emlp = line["my_team_estimate_league_point"]
            self.eolp = line["his_team_estimate_league_point"]
    def lists(self, ):
        list = []
        if self.mode == "gachi" and self.type == "standard":
            list = [self.id, self.version, self.map, self.mode, 
            self.rule, self.udemae, self.egp, self.time, self.ocount, self.mcount, self.knockout]
        # if self.mode == "regular" and self.type == "standard":
            # list = [self.id, self.mode, "turfwar", "-", "-", "-", "-" "-"]
        return list

# Write csv File
f = open("gachi.csv", "w", newline="")
w = csv.writer(f)

# Getting File List and Sorting
file = glob.glob("json/*.json")
file.sort()
# print(file)

result = []
for path in file:
    f = open(path, "r", encoding="utf-8")
    data = json.loads(f.read())

    for res in data:
        if res["automated"] == True:
            if len(Res(res).lists()) != 0:
                # print(Res(res).id)
                w.writerow(Res(res).lists())
    # break