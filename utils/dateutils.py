import datetime


#'2021-04-12T03:51:47.092Z'

def str_to_date_object(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')