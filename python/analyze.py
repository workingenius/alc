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
    
    def filter_out(self, tags, curline):
        tags = tags or []
        curline = curline or 1  # line number starts from 1

        new_line_lst = []
        for line in self.line_lst:
            if line.tag not in tags:
                new_line_lst.append(line.raw)
        return new_line_lst, 1
        

class Line(object):
    def __init__(self, raw, linenum, datetime, level, tag, procnum, content):
        self.raw = raw
        self.linenum = int(linenum)
        self.datetime = datetime
        self.level = level
        self.tag = tag
        self.procnum = int(procnum)
        self.content = content

