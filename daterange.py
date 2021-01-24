import argparse
import sys

from datetime import date
from datetime import timedelta

def daterange(*args):
    """
    daterange(stop) -> date generator
    daterange(start, stop[, step]) -> date generator

    Like `range` for dates. When start is omitted it defaults to today.
    """
    if len(args) == 1:
        stop = args[0]
        start = date.today()
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    elif len(args) == 3:
        start, stop, step = args
    step = timedelta(days=step)
    while start < stop:
        yield start
        start += step

def main(argv=None):
    "Generate a range of dates."
    parser = argparse.ArgumentParser(
        description=main.__doc__, prog='daterange', epilog=daterange.__doc__)
    parser.add_argument(
        'rangeargs', nargs='+', help="stop. start, stop[, step].")
    parser.add_argument(
        '-z', '--null', action='store_true',
        help="separate by null instead of newline")
    parser.add_argument(
        '-o', '--output', default=sys.stdout, help='output file')
    parser.add_argument(
        '-f', '--format', default='%Y-%m-%d', help='output date format')
    args = parser.parse_args(argv)

    if len(args.rangeargs) > 3:
        parser.error('one to three arguments required')

    rangeargs = [date.fromisoformat(arg) for arg in args.rangeargs[:2]]
    if len(args.rangeargs) == 3:
        rangeargs += [int(args.rangeargs[2])]

    sep = '\0' if args.null else '\n'

    g = (d.strftime(args.format) for d in daterange(*rangeargs))
    print(sep.join(g), end='', file=args.output)


if __name__ == '__main__':
    main()
