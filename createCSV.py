
""" 
Generates a CSV file containing the inputs to lambda.
"""

import csv
import pandas as pd

with open('recipientsInfo.csv', 'w') as file:
    writer = csv.writer(file)
    headers = ['email', 'city', 'timezone']

    writer.writerow(headers)

    writer.writerow(['samzitestemail@gmail.com', 'orrville', 'EDT'])
    writer.writerow(['aleksagavric1@gmail.com', 'charlotte', 'EDT'])