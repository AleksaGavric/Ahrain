#this file creates a new CSV file containing the info of who wants to be notified when rain is incoming
import csv
import pandas as pd


# open the file in the write mode
with open('recipientsInfo.csv', 'w') as file:
    writer = csv.writer(file)
    headers = ['email', 'city', 'timezone']

    #write headers
    writer.writerow(headers)

    #write recipients info, with each recipient on new row
    writer.writerow(['samzitestemail@gmail.com', 'orrville', 'EDT'])
    writer.writerow(['aleksagavric1@gmail.com', 'charlotte', 'EDT'])