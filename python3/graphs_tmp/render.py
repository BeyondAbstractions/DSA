import graphs
import graphviz
import collections
from graphs import loader
import argparse
import os


def get_graphviz_adjm(g: collections.OrderedDict) -> graphviz.Graph:
    g = graphs.UnDirectedGraph(g=graphs.UndirectedAdjMatrix(g=g)).graphviz()
    return g


def get_graphviz_adjl(g: collections.OrderedDict) -> graphviz.Graph:
    g = graphs.UnDirectedGraph(g=graphs.UndirectedAdjList(g=g)).graphviz()
    return g


def get_digraphviz_adjm(g: collections.OrderedDict) -> graphviz.Digraph:
    g = graphs.DirectedGraph(g=graphs.DirectedAdjMatrix(g=g)).graphviz()
    return g


def get_digraphviz_adjl(g: collections.OrderedDict) -> graphviz.Graph:
    g = graphs.DirectedGraph(g=graphs.DirectedAdjList(g=g)).graphviz()
    return g


def load_adj_list(args):
    g = loader.load_adj_list(args)
    filename = os.path.splitext(args.input)[0]
    if args.directed:
        get_digraphviz_adjl(g=g).render(filename=filename, format="svg", cleanup=True)
    else:
        get_graphviz_adjl(g=g).render(filename=filename, format="svg", cleanup=True)


def load_adj_matrix(args):
    g = loader.load_adj_matrix(args)
    filename = os.path.splitext(args.input)[0]
    if args.directed:
        get_digraphviz_adjm(g=g).render(filename=filename, format="svg", cleanup=True)
    else:
        get_graphviz_adjm(g=g).render(filename=filename, format="svg", cleanup=True)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Parse a filename from the command line."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    adjl_parser = subparsers.add_parser("adjl", help="Parse adj list.")

    adjm_parser = subparsers.add_parser("adjm", help="Parse adj matrix.")

    for p in (adjl_parser, adjm_parser):
        p.add_argument("input", type=str, help="Input file.")
        p.add_argument("--directed", action="store_true", help="Directed graph.")

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
