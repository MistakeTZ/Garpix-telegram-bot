import csv


def get_promo(promo: str):
    with open("promos.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            if line["promo"] == promo:
                return line
    
    return None