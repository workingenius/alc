from functools import wraps
import re

import vim
from analyze import analyze


def temp_modify(proc):
    @wraps(proc)
    def _proc_modify(*args, **kwargs):
        vim.command(":set modifiable")
        ret = proc(*args, **kwargs)
        vim.command(":set nomodifiable")
        return ret
    return _proc_modify


_origins = {}


def get_origin(buffer):
    return _origins.get(buffer.number)


def set_origin(buffer, origin):
    _origins[buffer.number] = origin


def del_origin(buffer):
    if buffer in _origins:
        _origins.pop(buffer.number)


def main(cmd, *args):
    vim.command(':set hidden')
    # check if working as a view
    onum = get_origin(vim.current.buffer)
    if onum is not None:
        print('This is a alc view')
        # if it is, the origin may have been deleted
        if onum in (b.number for b in vim.buffers):
            pass
        else:
            print('It\'s origin is removed')
            vim.command('bw')
    else:
        print('This is not a alc view, create one and copy contents')
        _analyzed[vim.current.buffer] = analyze(vim.current.buffer)
        contents = list(vim.current.buffer)
        onum = vim.current.buffer.number
        vim.command(':enew')
        cnum = vim.current.buffer.number
        set_origin(vim.current.buffer, onum)

        # copy from origin to here
        vim.current.buffer[:] = contents


    if cmd == 'ftag':
        cmd_ftag(*args)

    else:
        print('Unrecognized alc command {}'.format(cmd))


_analyzed = {}


_filter_out_tags = set()


@temp_modify
def cmd_ftag(*args):
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

    curcontents = vim.current.buffer
    line_lst, newcurline = _analyzed[vim.buffers[get_origin(vim.current.buffer)]].filter_out(_filter_out_tags, 1)
    if len(line_lst) != len(curcontents):
        vim.current.buffer[:] = line_lst

    # basecontents = list(vim.buffers[get_origin(vim.current.buffer)])
    # curcontents = vim.current.buffer
    # newcontents = []
    # ptn = re.compile('|'.join(sorted(_filter_out_tags)))
    # for line in basecontents:
    #     if not ptn.search(line):
    #         newcontents.append(line)

    # if len(newcontents) != len(curcontents):
    #     vim.current.buffer[:] = newcontents

