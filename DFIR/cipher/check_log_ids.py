import csv

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    print("Row | Log_ID")
    for i, row in enumerate(reader):
        print(f"{i+1} | {row['Log_ID']}")
        if i > 40: break # Just check the first few and the transition
