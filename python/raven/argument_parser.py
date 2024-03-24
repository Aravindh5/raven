

__author__ = 'Valtanix Inc.'

import sys
import argparse
import datetime


class ArgumentParser(object):
    """
    Parses input arguments
    """

    def start(self):
        print ('sys.argv')
        print (sys.argv)

        parser = argparse.ArgumentParser()
        parser.add_argument('--level', help='logging level')
        parser.add_argument('--time_start', help='start date . Must follow with <[Y-%m-%d]>. ')
        parser.add_argument('--time_stop', help='stop date . Must follow with <[Y-%m-%d]>. ')
        parser.add_argument('--incremental', help='[True|False. Set to true if connecting to Production.', choices=['True', 'False'])
        parser.add_argument('--dsa_url', required=False, help='REST url for DSA data set Eg: https://dsaweb-31-datastax-academy.pantheonsite.io/c360/updateC360/index.json')
        parser.add_argument('--dsa_oauth', required=False, help='Authendication for DSA data set Eg: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYWNhZGVteS5kYXRhc3RheC5jb20iLCJhdWQiOiJodHRwczpcL1wvYWNhZGVteS5kYXRhc3RheC5jb20iLCJqdGkiOiJpblg3YnQ1Q3U1Zy1vUk9MaTdpdEY0bEMtRV9iUk94akJNbG8tWFJDcUdZIiwiZXhwIjoxNTE4ODIyMDc5LCJuYmYiOjE1MTYyMzAwNzksImlhdCI6MTUxNjIzMDA3OSwiZW1haWwiOiJzeXNhZG1pbkBkYXRhc3RheC5jb20iLCJzdWIiOiI3NTgxY2FlOS0yMWZlLTQ4MWEtOTg4Zi01NzEzMWQwOTNkMjUifQ.aRrvAfXLcpx0VTv81eAGyhUEkNhUSLS4EQWLiFz9IMI')
        parser.add_argument('--c360_mysql_uri', help='MySQL Connection URI Eg: mysql://user:password!@127.0.0.1/database')
        parser.add_argument('--sfdc_mysql_uri', help='MySQL Connection URI Eg: mysql://user:password!@127.0.0.1/database')
        parser.add_argument('--academy_mysql_uri', help='MySQL Connection URI Eg: mysql://user:password!@127.0.0.1/database')
        parser.add_argument('--data_dir', help='directory of data folder')

        args = parser.parse_args()

        if args.level:
            print('arg: logging level: '.format(arg=args.level))

        if args.time_start:
            print('arg: start time: '.format(arg=args.time_start))
            try:
                datetime.datetime.strptime(args.time_start, '%Y-%m-%d')
            except ValueError:
               raise ValueError('--timestart argument must be a valid date of format YYYY-MM-DD')

        if args.time_stop:
            print('arg: stop time: '.format(arg=args.time_stop))
            try:
                datetime.datetime.strptime(args.time_stop, '%Y-%m-%d')
            except ValueError:
               raise ValueError('--timestop argument must be a valid date of format YYYY-MM-DD')

        if args.incremental:
            print('arg: incremental: {arg}'.format(arg=args.incremental))
            if args.incremental == 'True':
                args.incremental = True
            else:
                args.incremental = False

        if args.dsa_url:
            print('arg: rest_url: '.format(arg=args.dsa_url))

        if args.dsa_oauth:
            print('arg: rest_oauth: '.format(arg=args.dsa_oauth))

        if args.c360_mysql_uri:
            print('arg: C360 MySQL URI: ' + args.c360_mysql_uri)

        if args.sfdc_mysql_uri:
            print('arg: SFDC MySQL URI: ' + args.sfdc_mysql_uri)

        if args.academy_mysql_uri:
            print('arg: ACADEMY MySQL URI: ' + args.academy_mysql_uri)

        if args.data_dir:
            print('arg: data directory: ' + args.data_dir)

        return args.level, args.time_start, args.time_stop, args.incremental, args.dsa_url, args.dsa_oauth, args.c360_mysql_uri, args.sfdc_mysql_uri, args.academy_mysql_uri, args.data_dir


if __name__ == "__main__":
    sys.exit('Cannot be called as main()')

