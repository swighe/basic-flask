#!/usr/bin/python

class Product:
    def __init__(self, name, manufacturer, submission_date):
        self.name = name
        self.manufacturer = manufacturer
        self.submission_date = submission_date

    def __str__(self):
        # return '\{\{"name" : {}\},\{"manufacturer": {}\},\{"submission_date": {}}\\}'.format(self.name, self.manufacturer, self.submission_date)
        return 'name : {}, manufacturer: {}, submission_date: {}'.format(self.name, self.manufacturer, self.submission_date)