import csv

def checkdata(category3):
    with open("./rule_list.csv", encoding="utf-8_sig") as csvfile:
        rows = csv.reader(csvfile)

        for num, row in enumerate(rows, 1):
            if str(category3) == row[0]:
                value = row[1]
                return value

if __name__ =="__main__":
    category3 = 17
    value = checkdata(category3)
    print(value)