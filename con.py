"""con is a console application for using Alberlendar"""
import argparse
from alberlendar import Alberlendar

def main():
    parser = argparse.ArgumentParser(description='Process name of scoper')
    parser.add_argument('--scooper', '-s')
    parser.add_argument('--cal_id', '-c')
    parser.add_argument('--primary', '-p', action='store_true')
    args = parser.parse_args()

    if not args.scooper:
        args.scooper = input("What is your name on the schedule?:")

    if args.primary:
        args.cal_id = 'primary'

    return Alberlendar(args.scooper, args.cal_id)

if __name__ == '__main__':
    main()
