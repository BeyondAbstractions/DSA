import collections, argparse, csv, sys


def load_adj_list_impl(fp) -> collections.OrderedDict:
    g = collections.OrderedDict()
    for row in csv.reader(fp):
        g[row[0]] = row[1:]
    return g


def load_adj_list(args) -> collections.OrderedDict:
    filename = args.input
    ret = None
    if filename == "-":
        ret = load_adj_list_impl(sys.stdin)
    else:
        with open(file=filename) as fp:
            ret = load_adj_list_impl(fp)
    return ret


def load_adj_matrix_impl(fp) -> collections.OrderedDict:
    g = collections.OrderedDict()
    col = None
    for i, row in enumerate(csv.reader(fp)):
        i = i + 1
        g[i] = collections.OrderedDict()
        if col is None:
            col = len(row)
        else:
            assert col == len(row), "Should be a square matrix."

        for j, c in enumerate(row):
            j = j + 1
            c = c.strip()
            one = c == "1"
            zero = c == "0"
            assert one or zero, "Value should be 1/0."
            if one:
                g[i][j] = 1
            elif zero:
                g[i][j] = 0
    assert i == col, "Should be a square matrix."
    return g


def load_adj_matrix(args) -> collections.OrderedDict:
    filename = args.input
    ret = None
    if filename == "-":
        ret = load_adj_matrix_impl(sys.stdin)
    else:
        with open(file=filename) as fp:
            ret = load_adj_matrix_impl(fp)
    return ret


def get_parser():
    parser = argparse.ArgumentParser(
        description="Parse a filename from the command line."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    adjl_parser = subparsers.add_parser("adjl", help="Parse adj list.")

    adjm_parser = subparsers.add_parser("adjm", help="Parse adj matrix.")

    for p in (adjl_parser, adjm_parser):
        p.add_argument("input", type=str, help="Input file.")

    adjl_parser.set_defaults(func=load_adj_list)
    adjm_parser.set_defaults(func=load_adj_matrix)

    return parser


def main():

    parser = get_parser()

    args = parser.parse_args()
    ret = args.func(args)
    return ret


if __name__ == "__main__":
    main()
