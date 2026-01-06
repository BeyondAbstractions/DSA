#!/usr/bin/env python3
"""
HTML stepper debugger with process info and thread stacks.

Usage:
  python html_stepper.py a.b.c --args "[10]" --kwargs "{'verbose': True}" --include path/to/extra.py
"""

from __future__ import annotations

import ast
import bdb
import html
import importlib
import inspect
import collections
import linecache
import os
import shlex
import shutil
import sys
import textwrap
import threading
from argparse import ArgumentParser, Namespace
from pathlib import Path
from types import FrameType, ModuleType, TracebackType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
)
import time_travel_debugger.templates
import jinja2


class HtmlStepperDebugger(bdb.Bdb):
    """Bdb-based debugger that emits HTML snapshots for each line event."""

    def __init__(
        self, out_dir: str = "trace_out", include_files: Optional[Sequence[str]] = None
    ) -> None:
        bdb.Bdb.__init__(self=self)
        self.out_dir: Path = Path(out_dir)
        shutil.rmtree(self.out_dir, ignore_errors=True)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.step: int = 0
        self.snapshots: List[str] = []
        self.include: Set[str] = set(
            str(Path(f).resolve()) for f in (include_files or [])
        )
        self._source_cache: Dict[str, List[str]] = {}

    def user_line(self, frame: FrameType) -> None:
        bdb.Bdb.user_line(self=self, frame=frame)

        file_name: str = f"{self.step}.html"
        file_path: Path = self.out_dir.joinpath(file_name)

        previous_step = self.step - 1
        if previous_step < 0:
            previous_step = 0
        next_step = self.step + 1

        sections = collections.OrderedDict()
        sections["callstack"] = "Call Stack"
        sections["globals"] = "Globals"
        sections["locals"] = "Locals"
        sections["threads"] = "Threads"
        sections["visuals"] = "Visuals"

        with open(file=str(file_path), mode="w") as file_pointer:
            print(
                jinja2.Template(time_travel_debugger.templates.prefix_template).render(
                    title=f"Step: {self.step}",
                    current=f"{self.step}",
                    sections=sections,
                ),
                file=file_pointer,
            )

            for sid, sname in sections.items():
                print(
                    jinja2.Template(
                        time_travel_debugger.templates.section_template
                    ).render(
                        title=f"Step: {self.step}",
                        current=f"{self.step}",
                        sid=sid,
                        sname=sname,
                        lines=20,
                    ),
                    file=file_pointer,
                )

            print(
                f"[{self.step}] user_line: {frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno}"
            )

            print(
                jinja2.Template(
                    time_travel_debugger.templates.suffix_template
                ).render(),
                file=file_pointer,
            )
            self.out_dir.joinpath(f"{self.step}_previous.html").symlink_to(
                f"{previous_step}.html"
            )
            self.out_dir.joinpath(f"{self.step}_next.html").symlink_to(
                f"{next_step}.html"
            )
        self.step += 1

    def user_call(self, frame, argument_list):
        bdb.Bdb.user_call(self=self, frame=frame, argument_list=argument_list)
        print(
            f"[{self.step}] user_call: {frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno}"
        )

    def user_exception(
        self,
        frame: FrameType,
        exc_info: Tuple[type[BaseException], BaseException, Optional[TracebackType]],
    ) -> None:
        bdb.Bdb.user_exception(self=self, frame=frame, exc_info=exc_info)
        print(
            f"[{self.step}] user_exception: {frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno}"
        )

    def user_return(self, frame, return_value):
        bdb.Bdb.user_return(self=self, frame=frame, return_value=return_value)
        print(
            f"[{self.step}] user_return:  {frame.f_code.co_filename}:{frame.f_code.co_name}:{frame.f_lineno} -> {return_value}"
        )

    def finalize(self):
        last_step = self.step - 1
        if last_step < 0:
            last_step = 0
        self.out_dir.joinpath(f"begin.html").symlink_to(f"0.html")
        self.out_dir.joinpath(f"end.html").symlink_to(f"{last_step}.html")

        self.out_dir.joinpath(f"0_previous.html").unlink()
        self.out_dir.joinpath(f"0_previous.html").symlink_to(f"{last_step}.html")

        self.out_dir.joinpath(f"{last_step}_next.html").unlink()
        self.out_dir.joinpath(f"{last_step}_next.html").symlink_to(f"0.html")


# ---------- Entry point resolution ----------


def resolve_entrypoint(entry: str) -> Tuple[Callable[..., Any], ModuleType]:
    """
    Resolve 'a.b.c' into (callable, owning_module).
    Strategy: import the longest module prefix; traverse remaining attributes.
    """
    parts: List[str] = entry.split(".")
    last_err: Optional[Exception] = None
    for i in range(len(parts), 0, -1):
        mod_name: str = ".".join(parts[:i])
        try:
            mod: ModuleType = importlib.import_module(mod_name)
        except Exception as e:
            last_err = e
            continue
        obj: Any = mod
        for attr in parts[i:]:
            if not hasattr(obj, attr):
                raise AttributeError(
                    f"'{obj}' has no attribute '{attr}' while resolving '{entry}'"
                )
            obj = getattr(obj, attr)
        return obj, mod
    raise ImportError(f"Cannot resolve entry '{entry}': {last_err}")


def get_callable_file(func: Callable[..., Any]) -> str:
    """Return the source filename for a callable, falling back to its module file."""
    try:
        return str(Path(func.__code__.co_filename).resolve())
    except Exception:
        m = inspect.getmodule(func)
        return str(Path(getattr(m, "__file__", "unknown")).resolve())


# ---------- Runner ----------


def run_function(
    entry: str,
    args: Optional[Sequence[Any]] = None,
    kwargs: Optional[Mapping[str, Any]] = None,
    out_dir: str = "trace_out",
    include_files: Optional[Sequence[str]] = None,
) -> None:
    """Run the resolved entrypoint function under the HTML stepper debugger."""
    func, _mod = resolve_entrypoint(entry)
    if not callable(func):
        raise TypeError(f"Resolved object is not callable: {func}")

    main_file: str = get_callable_file(func)
    include_files = include_files or [main_file]

    dbg = HtmlStepperDebugger(out_dir=out_dir, include_files=include_files)

    try:
        dbg.runcall(func, *(args or []), **(kwargs or {}))
    except:
        pass
    finally:
        dbg.finalize()


# ---------- CLI ----------


def parse_args(argv: Sequence[str]) -> Namespace:
    """Parse CLI arguments for entrypoint, args/kwargs, and include list."""
    p: ArgumentParser = ArgumentParser(
        description="HTML stepper debugger for namespace entrypoints (a.b.c)"
    )
    p.add_argument("entry", help="Namespace entrypoint, e.g. package.module.function")
    p.add_argument("--out", default="trace_out", help="Output directory for HTML files")
    p.add_argument("--args", help="Positional args literal (e.g., \"[10, 'x']\")")
    p.add_argument(
        "--kwargs", help="Keyword args literal (e.g., \"{'verbose': True}\")"
    )
    p.add_argument(
        "--include", nargs="*", help="Additional files to include for stepping"
    )
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Main entry: parse CLI and run the target function under debugger."""
    opts: Namespace = parse_args(argv or sys.argv[1:])
    pos: List[Any] = ast.literal_eval(opts.args) if opts.args else []
    kw: Dict[str, Any] = ast.literal_eval(opts.kwargs) if opts.kwargs else {}
    inc: List[str] = [str(Path(f).resolve()) for f in (opts.include or [])]
    run_function(opts.entry, args=pos, kwargs=kw, out_dir=opts.out, include_files=inc)


if __name__ == "__main__":
    main()
