"""con is a console application for using Alberlendar"""
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process name of scoper')
    parser.add_argument('--scooper', '-s')
    args = parser.parse_args()
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
