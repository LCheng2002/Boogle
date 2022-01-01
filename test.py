import os
for root, ds, fs in os.walk("./first/0"):
    for f in fs:
        print(f)
        # indextxt = open("./first/0/"+f, 'r')