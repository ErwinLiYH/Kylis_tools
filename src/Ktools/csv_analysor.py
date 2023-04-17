import argparse
import pandas
import sys
from io import StringIO

def main():
    parser = argparse.ArgumentParser(description='csv analysor')
    parser.add_argument("--file", "-f", type=str, action="store", help="from file")
    parser.add_argument("--average", "-a", type=str, action="store", nargs="*", help="columns to average")
    parser.add_argument("--max", type=str, action="store", nargs="*", help="columns to max")
    parser.add_argument("--min", type=str, action="store", nargs="*", help="columns to min")
    parser.add_argument("--sd", type=str, action="store", nargs="*", help="columns to standard deviation")
    parser.add_argument("--basic", "-b", type=str, action="store", nargs="*", help="columns to standard deviation")

    args = parser.parse_args()

    S = "-----------------------------------------------------"

    if args.file:
        csv = pandas.read_csv(args.csv)
    else:
        csv = pandas.read_csv(StringIO(sys.stdin.read().strip()))

    res = [S]

    if args.basic!=None:
        args.average = [i for i in args.basic]
        args.max = [i for i in args.basic]
        args.min = [i for i in args.basic]
        args.sd = [i for i in args.basic]

    if args.average!=None:
        res.append("average:")
        if len(args.average)==0:
            res.append(csv.mean(numeric_only=True))
        else:
            res.append(csv[args.average].mean(numeric_only=True))
        res.append(S)

    if args.average!=None:
        res.append("max:")
        if len(args.average)==0:
            res.append(csv.max(numeric_only=True))
        else:
            res.append(csv[args.max].max(numeric_only=True))
        res.append(S)

    if args.average!=None:
        res.append("min:")
        if len(args.average)==0:
            res.append(csv.min(numeric_only=True))
        else:
            res.append(csv[args.min].min(numeric_only=True))
        res.append(S)

    if args.average!=None:
        res.append("standard deviation:")
        if len(args.average)==0:
            res.append(csv.std(numeric_only=True))
        else:
            res.append(csv[args.sd].std(numeric_only=True))
        res.append(S)

    for i in res:
        print(i)

if __name__=="__main__":
    main()

    