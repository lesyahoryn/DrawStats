import random
import csv

nr=36
nc=36
rows = range(nr)
cols = range(nc)
prob = 0.50
multiplier = 1000 #base is 5,000
om= [([0]*nr) for i in range(nc)]
im= [([0]*nr) for i in range(nc)]

ifile=open("stat.txt","r")

lines=ifile.readlines()
r=0
for l in lines:
    tmp=l.split()
    #print(tmp)
    c=0
    for t in tmp:
        #print(t)
        im[r][c]=round(float(t))
        c+=1
    r+=1

for r in rows:
    tmp=""
    for c in cols:
        tmp+="%s "%im[r][c]
    #print(f"%s"%tmp)

for r in rows:
    for c in cols:
        stat=im[r][c]
        for i in range(stat*multiplier):
            n=random.random()
            
            if n<prob:
                #home
                om[r][c]+=1
                #print(f"stat=%s, %s,%s:%s -> home"%(stat,r,c,n))
            else:
                #away
                om[c][r]+=1
                #print(f"stat=%s, %s,%s:%s -> away"%(stat,r,c,n))
        #print()

#csvfile = open("Data/Barbara/Ba{}Sim0.csv", 'w', newline='') 
f = open("Data/Barbara/Ba{}Sim0{}.csv".format(5*multiplier, str(prob).split('.')[-1]), 'w') 

for r in rows:
    tmp=""
    for c in cols:
        tmp+="%s, "%om[r][c]
    #csvfile.print("%s"%tmp)
    #spamwriter = csv.writer(csvfile, delimiter=',')
    #spamwriter.writerow(tmp)
    f.write("%s\n"%tmp)
#csvfile.close()
f.close()
