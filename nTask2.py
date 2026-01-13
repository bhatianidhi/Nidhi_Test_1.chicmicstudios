lfile = input("Enter log file name: ")

try:
    f = open(lfile, "r")
except FileNotFoundError:
    print("File not found")
    exit()

logs = []  
l_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0} 

flags = {"INFO": 1, "WARNING": 2, "ERROR": 4, "CRITICAL": 8}
important = flags["WARNING"] | flags["ERROR"] | flags["CRITICAL"]

for line in f:
    line = line.strip()
    if not line:
        continue

    parts = line.split(" - ")
    if len(parts) != 3:
        continue

    time = parts[0].strip()
    level = parts[1].strip()
    msg = parts[2].strip()

    logs.append({"time": time, "level": level, "msg": msg})

    if level in l_counts:
        l_counts[level] += 1

f.close()

print("\nLog Summary")
for level in l_counts:
    print(level, ":", l_counts[level])

print("\nImportant logs (WARNING, ERROR, CRITICAL):")
for log in logs:
    if flags.get(log["level"], 0) & important:
        print(log["time"], "-", log["level"], "-", log["msg"])

print("\nAll ERROR messages:")
for log in logs:
    if log["level"] == "ERROR" and len(log["msg"]) > 0:
        print("-", log["msg"])

print("\nTotal logs stored in list:", len(logs))
