"""con is a console application for using Alberlendar"""
import argparse
from alberlendar import Alberlendar

def main():
    parser = argparse.ArgumentParser(description='Process name of scoper')
    parser.add_argument('scooper')
    parser.add_argument('--cal_id', '-c')
    parser.add_argument('--primary', '-p', action='store_true')
    args = parser.parse_args()
    if args.scooper and args.cal_id:
        return Alberlendar(args.scooper, args.cal_id)


    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()