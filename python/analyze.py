import re

line_ptn = re.compile(r'^(?P<datetime>\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) (?P<level>[VDIWE])/(?P<tag>\w+)\s*\(\s*(?P<procnum>\d+)\s*\): (?P<content>.*)$')

def analyze(str_lst):
    # str_lst, each for a line
    lo_lst = []
    for i, line in enumerate(str_lst):
        i += 1  # line number starts from 1
        m = line_ptn.match(line)
        if m:
            g = m.groupdict()
            l = Line(line, i, g['datetime'], g['level'], g['tag'], g['procnum'], g['content'])
            lo_lst.append(l)
        elif line.startswith('---------'):
            l = Line(line, i, '', '', '', -1, '')
            lo_lst.append(l)
    return Analyzed(lo_lst)


class Analyzed(object):
    def __init__(self, line_lst):
        self.line_lst = list(line_lst)
        self.show_bm = [True] * len(line_lst)
        self._line_filter = None

    def filter(self, curline):
        if not self.line_filter:
            show_bm = [True] * len(self.line_lst)
            new_line_lst = [l.raw for l in self.line_lst]

        else:
            show_bm = []
            new_line_lst = []
            for line in self.line_lst:
                if self.line_filter.test(line):
                    show_bm.append(True)
                    new_line_lst.append(line.raw)
                else:
                    show_bm.append(False)

        cur_line = calc_curline(self.show_bm, show_bm, curline)
        self.show_bm = show_bm
        return new_line_lst, curline
    
    @property
    def line_filter(self):
        return self._line_filter

    @line_filter.setter
    def line_filter(self, v):
        self._line_filter = v


def calc_curline(old_show_bm, new_show_bm, curline):
    assert len(old_show_bm) == len(new_show_bm)
    # compare old show_bm and new, and know which line to jump to
    reaching = 0
    offset = 0
    for o, n in zip(old_show_bm, new_show_bm):
        if o:
            reaching += 1
        if reaching >= curline:
            curline += offset
            break
        if o and not n:
            offset -= 1
        elif not o and n:
            offset += 1
    return curline


assert calc_curline([True, True, True], [True, True, False], 1) == 1
assert calc_curline([True, True, True], [False, True, False], 1) == 1
assert calc_curline([True, True, True], [False, False, False], 1) == 1
assert calc_curline([True, True, True], [True, True, False], 2) == 2
assert calc_curline([True, True, True], [True, True, False], 3) == 3
assert calc_curline([True, True, True], [True, False, False], 3) == 2
assert calc_curline([False, True, True], [True, False, False], 2) == 2
assert calc_curline([False, True, True], [True, False, False], 1) == 2
        

class Line(object):
    def __init__(self, raw, linenum, datetime, level, tag, procnum, content):
        self.raw = raw
        self.linenum = int(linenum)
        self.datetime = datetime
        self.level = level
        self.tag = tag
        self.procnum = int(procnum)
        self.content = content

