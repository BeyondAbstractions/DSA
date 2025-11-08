import argparse
import graphviz
import sys
import jinja2
import re
import collections
import os


def track(func):
    def wrapper(*args, **kwargs):

        frame_id = None

        if not hasattr(wrapper, "seq"):
            wrapper.seq = 0

        if not hasattr(wrapper, "frame_id"):
            wrapper.frame_id = 0
        else:
            wrapper.frame_id += 1

        if not hasattr(wrapper, "depth"):
            wrapper.depth = 1
        else:
            wrapper.depth += 1

        if not hasattr(wrapper, "max_depth"):
            wrapper.max_depth = 1

        wrapper.max_depth = max(wrapper.max_depth, wrapper.depth)

        frame_id = wrapper.frame_id
        assert frame_id is not None

        params = f"{func.__name__}({', '.join(map(str, args))}"
        if kwargs:
            if args:
                params += ", "
            params += ", ".join(f"{k}={v}" for k, v in kwargs.items())
        params += ")"

        wrapper.seq += 1
        print(
            f"op:push#frame_id:{frame_id}#depth:{wrapper.depth}#fn:{params}#seq={wrapper.seq}"
        )

        result = func(*args, **kwargs)

        wrapper.seq += 1
        wrapper.depth -= 1
        print(
            f"op:pop#frame_id:{frame_id}#depth:{wrapper.depth}#fn:{params}#ret:{result}#max_depth:{wrapper.max_depth}#seq={wrapper.seq}"
        )

        return result

    return wrapper


def generate_topo_graph_svg_impl(topo_graph, filename):
    topo_svg = graphviz.Digraph()
    for frame in topo_graph:
        count = topo_graph[frame]["count"]
        topo_svg.node(name="%s, count=%s" % (frame, count))
    for src in topo_graph:
        src_count = topo_graph[src]["count"]
        edges = topo_graph[src]["edges"]
        for dest in edges:
            dest_count = topo_graph[dest]["count"]
            topo_svg.edge(
                tail_name="%s, count=%s" % (src, src_count),
                head_name="%s, count=%s" % (dest, dest_count),
            )
    topo_svg.render(filename=filename, format="svg", cleanup=True)


def generate_topo_graph_order_html_impl(
    topo_graph_normal, topo_graph_inverted, depth_problem_map, output_dir
):
    from html_templates import (
        prefix_template,
        suffix_template,
        table_start_template,
        table_end_template,
        topological_order_table_data_template,
        bottom_up_table_data_template,
        compressed_top_down_table_data_template,
        top_down_table_data_template,
    )

    with open(
        file=os.path.join(output_dir, "topological_traversal.html"), mode="w"
    ) as topo_traversal_fp, open(
        file=os.path.join(output_dir, "bottom_up.html"), mode="w"
    ) as bottom_up_fp, open(
        file=os.path.join(output_dir, "compressed_top_down.html"), mode="w"
    ) as compressed_top_down_fp, open(
        file=os.path.join(output_dir, "top_down.html"), mode="w"
    ) as top_down_fp:

        topo_traversal_fp.write(
            jinja2.Template(prefix_template).render(title="Topological Traversal")
        )
        topo_traversal_fp.write(
            jinja2.Template(table_start_template).render(
                table_headers=["Level", "Problems to solve"]
            )
        )

        current = collections.deque()
        nxt = collections.deque()
        level = 0

        for node in topo_graph_inverted:
            node_indgree = topo_graph_inverted[node]["indegree"]
            topo_graph_inverted[node]["indegree_copy"] = node_indgree
            if node_indgree == 0:
                current.append(node)

        topo_traversal_fp.write(
            jinja2.Template(topological_order_table_data_template).render(
                level=level, frames=current
            )
        )

        topo_order = list()

        while 1:

            if not current and not nxt:
                break

            node = current.popleft()
            topo_order.append(node)
            for neighbour in topo_graph_inverted[node]["edges"]:
                topo_graph_inverted[neighbour]["indegree_copy"] -= 1
                neighbour_indegree = topo_graph_inverted[neighbour]["indegree_copy"]
                if neighbour_indegree == 0:
                    nxt.append(neighbour)

            if not current:
                current, nxt = nxt, current
                if current:
                    level += 1
                    topo_traversal_fp.write(
                        jinja2.Template(topological_order_table_data_template).render(
                            level=level, frames=current
                        )
                    )

        topo_traversal_fp.write(jinja2.Template(table_end_template).render())
        topo_traversal_fp.write(jinja2.Template(suffix_template).render())
        topo_traversal_fp.flush()

        compressed_top_down_fp.write(
            jinja2.Template(prefix_template).render(
                title="Compressed top down solution for %s distinct problems:"
                % (len(topo_order))
            )
        )
        compressed_top_down_fp.write(
            jinja2.Template(table_start_template).render(
                table_headers=["Depth", "Problems"]
            )
        )
        compressed_top_down_fp.write(
            jinja2.Template(compressed_top_down_table_data_template).render(
                depth_problem_map=depth_problem_map
            )
        )
        compressed_top_down_fp.write(jinja2.Template(table_end_template).render())
        compressed_top_down_fp.write(jinja2.Template(suffix_template).render())
        compressed_top_down_fp.flush()

        top_down_fp.write(
            jinja2.Template(prefix_template).render(
                title="Top down solution for %s distinct problems:" % (len(topo_order))
            )
        )
        top_down_fp.write(
            jinja2.Template(table_start_template).render(
                table_headers=["Depth", "Problems"]
            )
        )
        top_down_fp.write(
            jinja2.Template(top_down_table_data_template).render(
                depth_problem_map=depth_problem_map,
                topo_graph=topo_graph_normal,
                enumerate=enumerate,
                hash=hash,
            )
        )
        top_down_fp.write(jinja2.Template(table_end_template).render())
        top_down_fp.write(jinja2.Template(suffix_template).render())
        top_down_fp.flush()

        bottom_up_fp.write(
            jinja2.Template(prefix_template).render(
                title="Bottom up solution for %s distinct problems:" % (len(topo_order))
            )
        )
        bottom_up_fp.write(
            jinja2.Template(table_start_template).render(
                table_headers=[
                    "Logical Time",
                    "Problem",
                    "Top Down Call Count",
                    "Dependent Problems",
                ]
            )
        )
        bottom_up_fp.write(
            jinja2.Template(bottom_up_table_data_template).render(
                topo_order=enumerate(topo_order), topo_graph=topo_graph_normal
            )
        )
        bottom_up_fp.write(jinja2.Template(table_end_template).render())
        bottom_up_fp.write(jinja2.Template(suffix_template).render())
        bottom_up_fp.flush()


def analyze_problem_state_impl(fp, output_dir):

    from html_templates import (
        prefix_template,
        suffix_template,
        table_start_template,
        call_stack_table_data_template,
        table_end_template,
    )

    with open(
        file=os.path.join(output_dir, "callstack.html"), mode="w"
    ) as callstack_html_fp:
        callstack_html_fp.write(
            jinja2.Template(prefix_template).render(title="Callstack")
        )
        callstack_html_fp.write(
            jinja2.Template(table_start_template).render(
                table_headers=["Logical Time", "Callstack"]
            )
        )

        call_graph = graphviz.Digraph()
        stack = list()
        logical_time = -1

        topo_graph = dict()
        topo_graph["normal"] = collections.OrderedDict()
        topo_graph["inverted"] = collections.OrderedDict()

        topo_graph_normal = topo_graph["normal"]
        topo_graph_inverted = topo_graph["inverted"]
        depth_problem_map = dict()

        for line in fp:
            split = line.strip().split("#")

            stack_op = split[0].strip().split("op:")[-1].lower()
            frame_id = int(split[1].strip().split("frame_id:")[-1])
            depth = int(split[2].strip().split("depth:")[-1])
            fn = split[3].strip().split("fn:")[-1]

            node_name = f"fid={frame_id}, {fn}"
            logical_time += 1

            if fn not in topo_graph_normal:
                topo_graph_normal[fn] = dict()
                topo_graph_normal[fn]["edges"] = collections.OrderedDict()
                topo_graph_normal[fn]["count"] = 0
                topo_graph_normal[fn]["indegree"] = 0
                topo_graph_normal[fn]["outdegree"] = 0

            if fn not in topo_graph_inverted:
                topo_graph_inverted[fn] = dict()
                topo_graph_inverted[fn]["edges"] = collections.OrderedDict()
                topo_graph_inverted[fn]["count"] = 0
                topo_graph_inverted[fn]["indegree"] = 0
                topo_graph_inverted[fn]["outdegree"] = 0

            if stack_op == "push":
                stack.append(node_name)
                call_graph.node(name=node_name)
                stack_len = len(stack)
                assert stack_len == depth

                topo_graph_normal[fn]["count"] += 1
                topo_graph_inverted[fn]["count"] += 1

                if stack_len not in depth_problem_map:
                    depth_problem_map[stack_len] = dict()
                    depth_problem_map[stack_len]["distinct"] = collections.OrderedDict()
                    depth_problem_map[stack_len]["nondistinct"] = dict()
                    depth_problem_map[stack_len]["nondistinct"]["problems"] = list()
                    depth_problem_map[stack_len]["nondistinct"][
                        "dependent"
                    ] = collections.OrderedDict()

                if fn not in depth_problem_map[stack_len]["distinct"]:
                    depth_problem_map[stack_len]["distinct"][fn] = 1
                else:
                    depth_problem_map[stack_len]["distinct"][fn] += 1

                depth_problem_map[stack_len]["nondistinct"]["problems"].append(
                    (node_name, stack[-2] if len(stack) >= 2 else "", fn)
                )

                if (stack_len - 1) in depth_problem_map:
                    if len(stack) >= 2:
                        if (
                            stack[-2]
                            not in depth_problem_map[stack_len - 1]["nondistinct"][
                                "dependent"
                            ]
                        ):
                            depth_problem_map[stack_len - 1]["nondistinct"][
                                "dependent"
                            ][stack[-2]] = [node_name]
                        else:
                            depth_problem_map[stack_len - 1]["nondistinct"][
                                "dependent"
                            ][stack[-2]].append(node_name)

                try:
                    call_graph.edge(
                        tail_name=stack[-2],
                        head_name=stack[-1],
                        label=f"seq={logical_time},",
                        color="blue",
                        fontcolor="blue",
                    )

                    from_node = re.sub(r"fid=\d+, ", "", stack[-2])
                    dest_node = re.sub(r"fid=\d+, ", "", stack[-1])

                    if dest_node not in topo_graph_normal[from_node]["edges"]:
                        topo_graph_normal[from_node]["edges"][dest_node] = None
                        topo_graph_normal[from_node]["outdegree"] += 1
                        topo_graph_normal[dest_node]["indegree"] += 1

                    if from_node not in topo_graph_inverted[dest_node]["edges"]:
                        topo_graph_inverted[dest_node]["edges"][from_node] = None
                        topo_graph_inverted[from_node]["indegree"] += 1
                        topo_graph_inverted[dest_node]["outdegree"] += 1

                except:
                    pass
            elif stack_op == "pop":
                ret = split[4].strip().split("ret:")[-1]
                max_depth = int(split[5].strip().split("max_depth:")[-1])
                try:
                    call_graph.edge(
                        tail_name=stack[-1],
                        head_name=stack[-2],
                        label=f"seq={logical_time}, ret={ret}",
                        color="red",
                        fontcolor="red",
                    )
                except:
                    call_graph.edge(
                        tail_name=stack[-1],
                        head_name=stack[-1],
                        label=f"seq={logical_time}, ret={ret}, max_depth={max_depth}",
                        color="red",
                        fontcolor="red",
                    )
                stack.pop()
            else:
                raise Exception(f"Unknown stack op: {split[0].upper()}")

            callstack_html_fp.write(
                jinja2.Template(call_stack_table_data_template).render(
                    logical_time=logical_time,
                    frames=map(lambda s: re.sub(r"fid=\d+, ", "", s), stack),
                )
            )

            callstack_html_fp.flush()

        callstack_html_fp.write(jinja2.Template(table_end_template).render())
        callstack_html_fp.write(suffix_template)
        callstack_html_fp.flush()

        call_graph.render(
            filename=os.path.join(output_dir, "callgraph"), format="svg", cleanup=True
        )

        generate_topo_graph_svg_impl(
            topo_graph=topo_graph_normal,
            filename=os.path.join(output_dir, "topological"),
        )
        generate_topo_graph_svg_impl(
            topo_graph=topo_graph_inverted,
            filename=os.path.join(output_dir, "topological_inverted"),
        )
        generate_topo_graph_order_html_impl(
            topo_graph_normal=topo_graph_normal,
            topo_graph_inverted=topo_graph_inverted,
            depth_problem_map=depth_problem_map,
            output_dir=output_dir,
        )


def analyze_problem_state(args):
    filename, output_dir = args.input, args.output_dir
    os.makedirs(name=output_dir, exist_ok=True)
    if filename == "-":
        analyze_problem_state_impl(sys.stdin, output_dir)
    else:
        with open(file=filename) as fp:
            analyze_problem_state_impl(fp, output_dir)


def generate_gdb_trace(args):
    pass


def main():
    parser = argparse.ArgumentParser(
        description="Parse a filename from the command line."
    )
    command_parser = parser.add_subparsers(dest="command", required=True)

    state_graph_parser = command_parser.add_parser(
        "analyze", help="Analyze track data."
    )
    state_graph_parser.add_argument(
        "input", type=str, help="Input file containing the stack trace."
    )
    state_graph_parser.add_argument(
        "output_dir",
        type=str,
        nargs="?",
        default="output",
        help="Output directory to dump analyzed track data (default: 'track').",
    )
    state_graph_parser.set_defaults(func=analyze_problem_state)

    gdb_graph_parser = command_parser.add_parser(
        "gdbtrace", help="Generate gdb trace (TODO)."
    )
    # gdb_graph_parser.add_argument("input", type=str, help="Input file ")
    # gdb_graph_parser.add_argument(
    #     "output",
    #     type=str,
    #     nargs="?",
    #     default="track",
    #     help="Output filename to dump the call graph (default: 'track').",
    # )
    gdb_graph_parser.set_defaults(func=generate_gdb_trace)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
