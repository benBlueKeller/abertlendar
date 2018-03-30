#! /usr/bin/python
"""con is a console application for using Alberlendar"""
import argparse
from salendar import Salendar

def main():
    parser = argparse.ArgumentParser(description='Process name of scoper')
    parser.add_argument('--scooper', '-s')
    parser.add_argument('--cal_id', '-c')
    parser.add_argument('--schedule_id', '-i')
    parser.add_argument('--primary', '-p', action='store_true')
    args = parser.parse_args()

    while not args.scooper:
        try:
            args.scooper = input("What is your name on the schedule?:")
        except NameError:
            print("NameError: try putting quotes around input")

    if not args.schedule_id:
        args.schedule_id = '1yGlxV9xSY6vk_d-WHoE9k18P06zfc7r8j975y5uvlJU'

    if args.primary:
        args.cal_id = 'primary'

    return Salendar(scooper=args.scooper,
                       cal_id=args.cal_id,
                       schedule_id=args.schedule_id)


if __name__ == '__main__':
    main()
