import sys


def print_help(msg=""):
    print(f"Usage: {sys.argv[0]} [-h] [--log LOG] [--base BASE] int [int ...]\n{msg}")


def main(args):
    integers = []
    log_file = ''
    base = 2

    while (args):
        arg = args.pop(0)
        if arg == '-h':
            print_help()
            return None, None
        elif arg == '--base':
            try:
                base = int(args.pop(0))
            except ValueError:
                print_help(f"invalid base value: {arg}")
                return None, None
        elif arg == '--log':
            log_file = args.pop(0)
        else:
            integers.append(arg)

    if not integers:
        print_help('No int args')
        return None, None

    try:
        return list(map(lambda x: int(x, base), integers)), log_file
    except ValueError as e:
        print_help(f"invalid value: {e}")
        return None, None


numbers, log_file = main(sys.argv[1:])

if log_file is None:
    pass
elif log_file == "":
    print(*numbers)
else:
    with open(log_file, "wt") as output:
        print(*numbers, file=output)