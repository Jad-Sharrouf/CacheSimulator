import math
import pandas as pd
import numpy as np
import sys

file = '1KB_64B' #sys.argv[1]
myFile = open(file,'r')
lines = myFile.readlines()

#Given: cache size, block size, ways
cacheSize = 1*1024 #bytes
addrBits = 12 #bits
lineSize = 64 #Bytes
ways = 16

method = 2 #0: direct, 1: fully, 2: set
sets = int(cacheSize/(lineSize*ways))

if method == 0 or method == 1:
    sets = 1

if method == 2 and sets == 1:
    method = 1

set_init = np.zeros((ways,), dtype=int)
slot_init = []
for x in range(ways):
    slot_init.append(x)
if sets > 1:
    for x in range(1,sets):
        set_init = np.concatenate((set_init,np.full((ways,), x, dtype=int)))
    
    slot_init = slot_init * sets 

tag_init = []
lru_init = []
data_init = []
for x in range(sets*ways):
    tag_init.append("")
    data_init.append("")
    lru_init.append(0)

d = {"set":set_init,"slot":slot_init,"tag":tag_init,"data":data_init,"LRU":lru_init}

#Direct-mapped cache doesn't use an LRU replacement policy
if method == 0:
    d = {"set":set_init,"slot":slot_init,"tag":tag_init,"data":data_init}

df = pd.DataFrame(data=d)


def binarySub(b1,b2):
    maxBits = max(len(b1), len(b2))
    return bin(int(b1, 2) - int(b2, 2))[2:].zfill(maxBits)
   

misses = 0
hits = 0
if method == 0:
    for line in lines:
        if len(line.strip()) == 0 :
            continue

        l = ""
        try:
            l = line.split()
            if len(l) != 3:
                continue
        except Exception:
            continue

        rw = l[1]
        addr = l[2][2:]

        #converting hex addr to binary
        try:
            addr = bin(int(addr, 16))[2:].zfill(addrBits)
        except Exception:
            continue
        
        #offset - 6 bits for 64B
        bits = int(math.log2(lineSize))
        offset = addr[-bits:]
        dataAddr = str(lineSize) + " bytes from @" + binarySub(addr,offset)
        #print(addr," -> ",offset)


        #index
        indexBits = int(math.log2(ways))
        index = addr[-bits-indexBits:-bits]
        index10 = int(index,2)
        #print(addr," -> ",index)

        #Tag
        tag = addr[:addrBits-(bits+indexBits)]
        #print(addr," -> ",tag)

        if df.at[index10,'tag'] == tag:
            hits += 1
        else:
            df.at[index10,'tag'] = tag
            df.at[index10,'data'] = dataAddr
            misses += 1
elif method == 1:
    for line in lines:
        if len(line.strip()) == 0 :
            continue
        
        l = ""
        try:
            l = line.split()
            if len(l) != 3:
                continue
        except Exception:
            continue

        rw = l[1]
        addr = l[2][2:]

        #converting hex addr to binary
        try:
            addr = bin(int(addr, 16))[2:].zfill(int(addrBits))
        except Exception:
            continue

        #offset - 6 bits for 64B
        bits = int(math.log2(lineSize))
        offset = addr[-bits:]
        dataAddr = str(lineSize) + " bytes from @" + binarySub(addr,offset)
        #print(addr," -> ",offset)

        #Tag
        tag = addr[:addrBits-bits]
        #print(addr," -> ",tag)

        checkTag = np.array(df['tag'])
        checklru = np.array(df['LRU'])

        if tag in checkTag:
            hits += 1
            hitIndex = np.where(checkTag==tag)
            hitIndex = hitIndex[0][0]
            df.at[hitIndex,'LRU'] = 0
            df.at[hitIndex,'data'] = dataAddr
        else:
            if "" in checkTag:
                emptyIndex = np.where(checkTag=="")
                emptyIndex = emptyIndex[0][0]
                df.at[emptyIndex,'tag'] = tag
                df.at[emptyIndex,'LRU'] = 0
                df.at[emptyIndex,'data'] = dataAddr
            else:
                victim = np.argmin(checklru)
                df.at[victim,'tag'] = tag
                df.at[victim,'LRU'] = 0
                df.at[victim,'data'] = dataAddr
            misses += 1

        lruIndex = np.where((df['tag'] != tag) & (df['tag'] != ""))
        for i in lruIndex[0]:
            df.at[i,'LRU'] -= 1
elif method == 2:
    for line in lines:
        if len(line.strip()) == 0 :
            continue
        
        l = ""
        try:
            l = line.split()
            if len(l) != 3:
                continue
        except Exception:
            continue

        rw = l[1]
        addr = l[2][2:]

        #converting hex addr to binary
        try:
            addr = bin(int(addr, 16))[2:].zfill(int(addrBits))
        except Exception:
            continue

        #offset - 6 bits for 64B
        bits = int(math.log2(lineSize))
        offset = addr[-bits:]
        #print(addr," -> ",offset)

        setIndexBits = int(math.log2(sets))

         #index
        setIndex = addr[-bits-setIndexBits:-bits]
        setIndex = int(setIndex,2)

        #Tag
        tag = addr[:addrBits-(bits+setIndexBits)]
        #print(addr," -> ",tag)
        
        dfSet = df[df['set'] == setIndex]
        checkTag = np.array(dfSet['tag'])
        checklru = np.array(dfSet['LRU'])

        if tag in checkTag:
            hits += 1
            hitIndex = np.where(checkTag==tag)
            hitIndex = hitIndex[0][0]
            hitIndex = setIndex*ways + hitIndex
            df.at[hitIndex,'LRU'] = 0
        else:
            if "" in checkTag:
                emptyIndex = np.where(checkTag=="")
                emptyIndex = emptyIndex[0][0]
                emptyIndex = setIndex*ways + emptyIndex
                df.at[emptyIndex,'tag'] = tag
                df.at[emptyIndex,'LRU'] = 0
            else:
                victim = np.argmin(checklru)
                victim = setIndex*ways + victim
                df.at[victim,'tag'] = tag
                df.at[victim,'LRU'] = 0
            misses += 1

        lruIndex = np.where((df['set'] == setIndex) & (df['tag'] != tag) & (df['tag'] != ""))
        for i in lruIndex[0]:
            df.at[i,'LRU'] -= 1

print(df)
missRate = (misses/(misses+hits)) * 100
cacheType = "Set-Associative"
if method == 0:
    cacheType = "Direct-Mapped"
elif method == 1:
    cacheType = "Fully-Associative" 
print("\nCache miss rate = {0}% using a {1} cache.".format(round(missRate, 2),cacheType))
