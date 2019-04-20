# coding:utf-8

import csv
import numpy as np
import matplotlib.pyplot as plt

class Stage:
    def __init__(self, id):
        self.id = id
        self.cwin = [0] * 101
        self.clos = [0] * 101
        self.win = [0] * 100
        self.los = [0] * 100
        self.avgwin = [0] * 101
        self.avglos = [0] * 101
        self.ratio = [0] * 101
        self.offset = 0
        self.game = 0
        self.count = []
        self.sprob = []
        self.wprob = []

    def add(self, line):
        self.game += 1

        if int(line[8]) > int(line[9]):
            w = int(line[8])
            l = int(line[9])
        else:
            w = int(line[9])
            l = int(line[8])
        
        self.cwin[w] += 1
        self.clos[l] += 1

        # ノックアウト勝ちしているか
        if line[10] == "TRUE":
            # 延長しているか
            if int(line[7]) > 300:
                # ノックアウトで延長勝利はカウント99が逆転負け
                self.los[99] += 1
            else:
                self.offset += 1
        else:
            if w - l == 1:
                # 敗北側カウントが延長入った段階で優勢だったものの逆転負け
                self.los[l] += 1
            else:
                if int(line[7]) <= 330:
                    try:
                        self.win[w] += 1
                    except IndexError:
                    # ノックアウト勝ちのエラー判定
                        self.offset += 1

    def val(self,):
        # プロットする範囲を調べる(勝利側上位75%を採用する)
        val = 0
        bk = 99
        while val + self.offset < int(self.game * 0.90):
            try:
                val += (self.win[bk] + self.los[bk])
            except IndexError:
                print("Error!")
                exit(1)
            bk -= 1
        self.count = [None] * bk
        self.sprob = [None] * bk
        self.wprob = [None] * bk

        num = sum(self.win[0:100])

        for k in range(bk, 100):
            self.sprob.append(sum(self.win[0:k]) / num)
            try:
                prob = sum(self.cwin[k-2:k+2]) / (sum(self.cwin[k-2:k+2]) + sum(self.clos[k-2:k+2]))
                if prob <= 0.6:
                    self.wprob.append(None)
                else:
                    self.wprob.append(prob)
            except ZeroDivisionError:
                self.wprob.append(None)

            for j in range(-2, 2):
                try:
                    self.avgwin[k] += self.win[k+j]
                except IndexError:
                    self.avgwin[k] += 0
                try:
                    self.avglos[k] += self.los[k+j]
                except IndexError:
                    self.avglos[k] += 0 
            try:
                self.ratio[k] = round(self.avgwin[k] / (self.avgwin[k] + self.avglos[k]), 4)
            except ZeroDivisionError:
                self.ratio[k] = 0
            self.count.append(self.ratio[k])
        self.count.append(1)
        self.sprob.append(1)
        self.wprob.append(1)
    
    def export(self):
        count = [self.id]
        for k in range (0, 100):
            try:
                count.append(self.ratio[k])
                # count.append(round(self.win[k] / (self.win[k] + self.los[k]), 4) )
            except ZeroDivisionError:
                count.append(0)
        count.append(1)
        return count
            
# main
stage = []

for id in range(0, 23):
    stage.append(Stage(id))

# Input
print("1: Splat Zones")
print("2: Tower Control")
print("3: Rainmaker")
print("4: Clam Blitzi")

type = input("Input the number >>")

if type == "1":
    mode = "Splat Zones"
    name = "sz_"
if type == "2":
    mode = "Tower Control"
    name = "tc_"
if type == "3":
    mode = "Rainmaker"
    name = "rm_"
if type == "4":
    mode = "Clam Blitz"
    name = "cb_"

with open("440.csv") as f:
    reader = csv.reader(f, delimiter=",", quotechar="'")
    for line in reader:
        if line[4] == mode and (line[5] == "s+" or line[5] == "x"):
            # Stage Selection
            stage[int(line[2])].add(line)

    f = open(mode+".csv", "w", newline="")
    w = csv.writer(f)

    header = ["id"]
    for k in range(0, 101):
        header.append(k)
    w.writerow(header)

    for id in range(0, 23):
        stage[id].val()
    
        x = np.linspace(1, 100, 101)
        y1 = stage[id].count
        # y2 = stage[id].sprob
        y3 = stage[id].wprob
        plt.clf()
        plt.figure(num=None, figsize=(12.8, 7.2))
        plt.tick_params(labelsize=18)
        # plt.ylim(0.5, )
        plt.grid()
        # plt.xticks(np.arange(0,100+1, 2))
        plt.ylabel("probability[%]", fontsize=18)
        plt.xlabel("count", fontsize=18)
        plt.plot(x, y1, label="Def[%]", linewidth=3)
        # plt.plot(x, y2, label="???", linewidth=3)
        plt.plot(x, y3, label="Win[%]", linewidth=3)
        plt.legend(fontsize=18)
        plt.savefig(name + str(stage[id].id) + ".png")
        plt.close()
        
        # CSV Writing
        w.writerow(stage[id].export())
    # plt.show()