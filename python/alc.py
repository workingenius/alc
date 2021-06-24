from functools import wraps
import re

import vim
from analyze import analyze
from bufferwrapper import BufferWrapper as BW
from linepred import *


def temp_modify(proc):
    @wraps(proc)
    def _proc_modify(*args, **kwargs):
        vim.command(":set modifiable")
        ret = proc(*args, **kwargs)
        vim.command(":set nomodifiable")
        return ret
    return _proc_modify


def main(*args):
    vim.command(':set hidden')
    bw = BW(vim.current.buffer)
    if not bw.is_prepared:
        bw.prepare()

    if args:
        cmd = args[0]
        args = args[1:]
    else:
        return

    if cmd == 'ftag':
        cmd_ftag(*args)

    else:
        print('Unrecognized alc command {}'.format(cmd))


@temp_modify
def cmd_ftag(*args):
    _analyzed = BW.current().analyzed

    _filter_out_tags = getattr(_analyzed, 'filter_out_tags', None)
    if _filter_out_tags is None:
        setattr(_analyzed, 'filter_out_tags', set())
        _filter_out_tags = getattr(_analyzed, 'filter_out_tags', None)

    if len(args) == 0:
        print(sorted(_filter_out_tags))
        return

    def ftagcmds():
        for arg in args:
            for seg in arg.split(','):
                yield seg

    old_fot = set(_filter_out_tags)

    for seg in ftagcmds():
        if seg.endswith('-'):
            tag = seg[:-1]
            _filter_out_tags.add(tag)
        elif seg.endswith('+'):
            tag = seg[:-1]
            if tag in _filter_out_tags:
                _filter_out_tags.remove(tag)
        else:
            print('<tag>+ for show lines with tag or <tag>- for hide lines with tag')

    if old_fot != _filter_out_tags:
        pass

    line_filter = LPBanned([LPTag(tag) for tag in _filter_out_tags])
    _analyzed.line_filter = line_filter if _filter_out_tags else None

    curcontents = vim.current.buffer
    line_lst, newcurline = _analyzed.filter(vim.current.window.cursor[0])
    if len(line_lst) != len(curcontents):
        vim.current.buffer[:] = line_lst
        vim.command(': {}'.format(newcurline))

