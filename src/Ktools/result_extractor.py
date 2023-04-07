import re
import argparse
import pandas

def extract_numbers(input_string):
    # Regular expression pattern to match integers and float values
    pattern = r"[-+]?\d*\.\d+|[-+]?\d+"
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)

    # Convert the matched strings to integers or floats
    numbers = [float(x) if "." in x else int(x) for x in matches]
    return numbers

def main():
    try:
        parser = argparse.ArgumentParser(description='result extructor, extruct data fome txt and convert to csv')
        parser.add_argument("infile", type=str, action="store", help="input raw text file path")
        parser.add_argument("outfile", type=str, action="store", help="output csv file path")
        parser.add_argument("starts", type=str, action="store", nargs="*", help="used to locate target line: line.startswith(<starts>)")
        parser.add_argument("--index", "-i", type=int, action="store", nargs="*", help="if multiple number in a target line, use witch one. defult: 0")
        parser.add_argument("--names", "-n", type=str, action="store", nargs="*", help="the names of each colume. default: <starts>")

        args = parser.parse_args()

        if args.names != None:
            if len(args.starts) != len(args.names):
                print("length of names must equals to length of starts!!!")
                return
        else:
            args.names = [i for i in args.starts]

        if args.index != None:
            if len(args.starts) != len(args.index):
                print("length of index must equals to length of starts!!!")
                return
        else:
            args.index = [0 for _ in range(len(args.starts))]

        data_dict = {i:[] for i in args.names}

        with open(args.infile, "r") as f:
            for line in f:
                for i in args.starts:
                    if line.startswith(i):
                        temp = extract_numbers(line)[args.index[args.starts.index(i)]]
                        data_dict[args.names[args.starts.index(i)]].append(temp)
                
        csv = pandas.DataFrame(data_dict)
        csv.to_csv(args.outfile, index=False)
    except ValueError as ve:
        print(ve)
        print("failed, please rnsure each column of data have same length!!!!")
    except KeyboardInterrupt:
        print("\nForce quit")

if __name__=="__main__":
    main()