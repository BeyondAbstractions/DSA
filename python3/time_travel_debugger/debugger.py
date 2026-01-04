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
import linecache
import os
import shlex
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

# ---------- Utilities ----------


def safe_repr(value: Any, maxlen: int = 200) -> str:
    """Return repr(value), truncated to maxlen, with a safe fallback."""
    try:
        s = repr(value)
    except Exception as e:  # pragma: no cover (rare repr errors)
        s = f"<repr error: {e}>"
    return s if len(s) <= maxlen else (s[: maxlen - 3] + "...")


def h(s: Any) -> str:
    """HTML-escape a string-like value safely."""
    return html.escape(str(s), quote=True)


def load_source_lines(filename: str) -> List[str]:
    """Read source file and return its lines; fallback to a placeholder on failure."""
    try:
        return Path(filename).read_text(encoding="utf-8").splitlines()
    except Exception:
        return [f"(source unavailable for {filename})"]


def source_line(filename: str, lineno: int) -> str:
    """Retrieve a single source line via linecache, with manual fallback."""
    try:
        line = linecache.getline(filename, lineno)
        if not line and Path(filename).exists():
            lines = load_source_lines(filename)
            return lines[lineno - 1] if 1 <= lineno <= len(lines) else ""
        return line or ""
    except Exception:
        return ""


def render_table(title: str, mapping: Mapping[str, Any]) -> str:
    """Render a simple key/type/value table for locals/globals."""
    rows: List[str] = [
        f"<h3>{h(title)}</h3>",
        "<table class=vars>",
        "<thead><tr><th>Name</th><th>Type</th><th>Value</th></tr></thead>",
        "<tbody>",
    ]
    for k, v in sorted(mapping.items(), key=lambda kv: kv[0]):
        if str(k).startswith("__"):  # reduce noise
            continue
        rows.append(
            "<tr>"
            f"<td>{h(k)}</td>"
            f"<td>{h(type(v).__name__)}</td>"
            f"<td><code>{h(safe_repr(v))}</code></td>"
            "</tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def render_code(source_lines: Sequence[str], current_lineno: int) -> str:
    """Render the source code table with the current line highlighted."""
    out: List[str] = ["<h3>Source</h3>", "<table class=code>", "<tbody>"]
    for i, line in enumerate(source_lines, start=1):
        cls = "current" if i == current_lineno else ""
        out.append(
            f"<tr class='{cls}'>"
            f"<td class='lineno'>{i}</td>"
            f"<td class='code-line'><pre>{h(line.rstrip())}</pre></td>"
            "</tr>"
        )
    out.append("</tbody></table>")
    return "\n".join(out)


def render_process_info() -> str:
    """Render process-level information: PID/PPID/argv/#threads."""
    pid: int = os.getpid()
    try:
        ppid: Any = os.getppid()
    except Exception:
        ppid = "(unavailable)"
    cmdline: str = " ".join(shlex.quote(a) for a in sys.argv)
    threads: List[threading.Thread] = threading.enumerate()
    rows: List[str] = [
        "<h3>Process Info</h3>",
        "<table class=proc>",
        "<thead><tr><th>PID</th><th>PPID</th><th>Cmdline</th><th>#Threads</th></tr></thead>",
        "<tbody>",
        f"<tr><td>{h(pid)}</td><td>{h(ppid)}</td><td><code>{h(cmdline)}</code></td><td>{len(threads)}</td></tr>",
        "</tbody></table>",
    ]
    return "\n".join(rows)


def frame_to_tuple(fr: FrameType) -> Tuple[str, int, str, str]:
    """Return (filename, lineno, funcname, line_text) for a frame."""
    try:
        fn = str(Path(fr.f_code.co_filename).resolve())
    except Exception:
        fn = getattr(fr.f_code, "co_filename", "unknown")
    ln: int = getattr(fr, "f_lineno", 0)
    func: str = getattr(fr.f_code, "co_name", "?")
    text: str = source_line(fn, ln).rstrip()
    return fn, ln, func, text


def walk_stack_from_top(top_frame: FrameType) -> List[FrameType]:
    """Return a stack list from root -> top for a given thread."""
    stack: List[FrameType] = []
    fr: Optional[FrameType] = top_frame
    while fr is not None:
        stack.append(fr)
        fr = fr.f_back
    stack.reverse()
    return stack


def render_thread_stacks(
    current_file: Optional[str] = None, current_lineno: Optional[int] = None
) -> str:
    """
    Render per-thread call stacks with thread metadata.
    Highlights the current location (file+line) for the current thread.
    """
    frames: Dict[int, FrameType] = sys._current_frames()  # {tid: frame}
    threads: Dict[int, threading.Thread] = {
        t.ident: t for t in threading.enumerate() if t.ident is not None
    }

    out: List[str] = ["<h3>Thread Stacks</h3>"]
    if not frames:
        out.append("<p class='dim'>(no active frames)</p>")
        return "\n".join(out)

    def sort_key(item: Tuple[int, Optional[threading.Thread]]) -> Tuple[int, str]:
        tid, thr = item
        main_first: int = 0 if (thr and thr.name == "MainThread") else 1
        name: str = thr.name if thr else str(tid)
        return (main_first, name)

    items: List[Tuple[int, Optional[threading.Thread]]] = sorted(
        [(tid, threads.get(tid)) for tid in frames.keys()], key=sort_key
    )

    for tid, thr in items:
        top: Optional[FrameType] = frames.get(tid)
        if top is None:
            # Thread exists but no frame; rare, skip rendering table.
            out.append(
                f"<div class='thread-heading'>Thread: <strong>{h(thr.name if thr else f'TID-{tid}')}</strong> (no frame)</div>"
            )
            continue

        name: str = thr.name if thr else f"TID-{tid}"
        daemon: bool = thr.daemon if thr else False
        alive: bool = thr.is_alive() if thr else True

        out.append(
            f"<div class='thread-heading'>Thread: <strong>{h(name)}</strong> "
            f"(tid={tid}, daemon={daemon}, alive={alive})</div>"
        )
        out.append("<table class=stack>")
        out.append(
            "<thead><tr><th>File</th><th>Line</th><th>Function</th><th>Code</th></tr></thead>"
        )
        out.append("<tbody>")
        for fr in walk_stack_from_top(top):
            fn, ln, func, text = frame_to_tuple(fr)
            cls = ""
            if (
                current_file
                and current_lineno
                and Path(fn).resolve() == Path(current_file).resolve()
                and ln == current_lineno
                and thr
                and thr.ident == threading.get_ident()
            ):
                cls = "here"  # highlight current snapshot location for current thread
            out.append(
                f"<tr class='{cls}'>"
                f"<td class='file'><code>{h(fn)}</code></td>"
                f"<td class='lineno'>{ln}</td>"
                f"<td class='func'>{h(func)}</td>"
                f"<td class='code'><pre>{h(text)}</pre></td>"
                "</tr>"
            )
        out.append("</tbody></table>")
    return "\n".join(out)


def base_html(
    title: str,
    body: str,
    prev_href: Optional[str] = None,
    next_href: Optional[str] = None,
) -> str:
    """Compose a full HTML document page with navigation and inline styles."""
    nav: List[str] = ["<div class=nav>"]
    nav.append(
        f"{prev_href}◀ Prev</a>"
        if prev_href
        else "<span class='btn disabled'>◀ Prev</span>"
    )
    nav.append(
        f"{next_href}Next ▶</a>"
        if next_href
        else "<span class='btn disabled'>Next ▶</span>"
    )
    nav.append("</div>")

    style: str = textwrap.dedent(
        """
    <style>
      body { font-family: ui-sans-serif, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
      .nav { margin: 1rem 0; display: flex; gap: 1rem; }
      .btn { padding: 0.4rem 0.8rem; border: 1px solid #888; border-radius: 6px; text-decoration: none; color: #222; background: #f5f5f5; }
      .btn.disabled { color: #999; background: #eee; border-color: #ccc; }
      table.code { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
      table.code td { vertical-align: top; }
      td.lineno { width: 3rem; text-align: right; color: #777; border-right: 1px solid #ddd; padding-right: 0.5rem; }
      td.code-line { padding-left: 0.5rem; }
      tr.current { background: #fffbd1; }
      table.vars, table.proc, table.stack { border-collapse: collapse; width: 100%; margin-top: 1rem; }
      table.vars th, table.vars td, table.proc th, table.proc td, table.stack th, table.stack td { border: 1px solid #ddd; padding: 0.4rem 0.6rem; vertical-align: top; }
      table.vars th, table.proc th, table.stack th { background: #f0f0f0; }
      table.proc td code, table.stack td code { white-space: pre-wrap; }
      code { white-space: pre-wrap; }
      .meta { color: #555; margin-bottom: 0.5rem; }
      .dim { color: #777; }
      .thread-heading { margin-top: 1.2rem; font-size: 0.95rem; color: #333; }
      table.stack td.file { width: 40%; }
      table.stack td.code pre { margin: 0; }
      tr.here { background: #e6ffea; } /* current location on current thread */
    </style>
    """
    )
    return (
        "<html><head><meta charset='utf-8'><title>"
        + h(title)
        + "</title>"
        + style
        + "</head><body>"
        + f"<h1>{h(title)}</h1>"
        + "\n".join(nav)
        + body
        + "\n".join(nav)
        + "</body></html>"
    )


# ---------- Debugger ----------


class HtmlStepperDebugger(bdb.Bdb):
    """Bdb-based debugger that emits HTML snapshots for each line event."""

    def __init__(
        self, out_dir: str = "trace_out", include_files: Optional[Sequence[str]] = None
    ) -> None:
        super().__init__()
        self.out_dir: Path = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.step: int = 0
        self.snapshots: List[str] = []
        self.include: Set[str] = set(
            str(Path(f).resolve()) for f in (include_files or [])
        )
        self._source_cache: Dict[str, List[str]] = {}  # filename -> [lines]

    def _get_lines(self, filename: str) -> List[str]:
        fn = str(Path(filename).resolve())
        if fn not in self._source_cache:
            self._source_cache[fn] = load_source_lines(fn)
        return self._source_cache[fn]

    def _page_for_frame(
        self, frame: FrameType, title_prefix: str, predictive_next: bool = True
    ) -> None:
        filename = str(Path(frame.f_code.co_filename).resolve())
        lineno: int = frame.f_lineno
        self.step += 1
        prev_href: Optional[str] = (
            f"step_{self.step - 1:04d}.html" if self.step > 1 else None
        )
        next_href: Optional[str] = (
            f"step_{self.step + 1:04d}.html" if predictive_next else None
        )

        meta: str = (
            f"<div class='meta'>"
            f"File: {h(filename)} &nbsp;|&nbsp; Line: {lineno} &nbsp;|&nbsp; Function: {h(frame.f_code.co_name)}"
            f"</div>"
        )

        body: str = (
            meta
            + render_code(self._get_lines(filename), lineno)
            + render_process_info()
            + render_thread_stacks(current_file=filename, current_lineno=lineno)
            + render_table("Locals", frame.f_locals)
            + render_table("Globals", frame.f_globals)
        )
        page: str = base_html(
            title=f"{title_prefix} {self.step:04d} — {Path(filename).name}:{lineno}",
            body=body,
            prev_href=prev_href,
            next_href=next_href,
        )
        out: Path = self.out_dir / f"step_{self.step:04d}.html"
        out.write_text(page, encoding="utf-8")
        self.snapshots.append(out.name)

    def user_line(self, frame: FrameType) -> None:
        filename = str(Path(frame.f_code.co_filename).resolve())
        if self.include and filename not in self.include:
            return
        self._page_for_frame(frame, title_prefix="Step", predictive_next=True)

    def user_exception(
        self,
        frame: FrameType,
        exc_info: Tuple[type[BaseException], BaseException, Optional[TracebackType]],
    ) -> None:
        filename = str(Path(frame.f_code.co_filename).resolve())
        if self.include and filename not in self.include:
            return
        etype, evalue, _tb = exc_info
        self._page_for_frame(
            frame,
            title_prefix=f"Exception ({etype.__name__}: {h(safe_repr(evalue))}) at",
            predictive_next=False,
        )

    def finalize_index(self) -> None:
        items: List[str] = [
            f"<li>{name}{h(name)}</a></li>" for name in self.snapshots
        ] or ["<li>(no steps)</li>"]
        index: str = base_html(
            "Trace Index", "<h3>All steps</h3><ol>" + "\n".join(items) + "</ol>"
        )
        (self.out_dir / "index.html").write_text(index, encoding="utf-8")


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
    finally:
        dbg.finalize_index()


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
