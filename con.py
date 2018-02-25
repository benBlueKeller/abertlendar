#! /usr/bin/python
"""con is a console application for using Alberlendar"""
import argparse
from alberlendar import Alberlendar

def main():
    parser = argparse.ArgumentParser(description='Process name of scoper')
    parser.add_argument('--scooper', '-s')
    parser.add_argument('--cal_id', '-c')
    parser.add_argument('--schedule_id', '-i')
    parser.add_argument('--primary', '-p', action='store_true')
    args = parser.parse_args()

    if not args.scooper:
        args.scooper = input("What is your name on the schedule?:")

    if args.primary:
        args.cal_id = 'primary'

    return Alberlendar(scooper=args.scooper,
                       cal_id=args.cal_id,
                       schedule_id=args.schedule_id)


if __name__ == '__main__':
    main()
