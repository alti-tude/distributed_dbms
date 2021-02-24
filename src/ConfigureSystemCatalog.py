import csv


def readSysCatalogCSV(input_file):
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)


if __name__ == '__main__':
    readSysCatalogCSV('../../trial.csv')