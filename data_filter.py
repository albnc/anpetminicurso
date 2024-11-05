import os

detectores = [401581, 401578, 401586, 410099, 401660,409885, 409883, 410116]
infolder = "C:\\temp\\pems\\"
for f in os.listdir(infolder):
    if not f.endswith(".txt"):
        continue

    out_lines = []

    with open(infolder+f, 'r') as file:
        for line in file.readlines():
            d = line.split(",")
            if int(d[1]) in detectores:
                out_lines.append(line)
    
    with open(infolder+"filtered_"+f, 'w') as file:
        file.writelines(out_lines)