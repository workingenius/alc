class LinePred(object):
    def test(self, line):
        raise NotImplementedError

    def __and__(self, other):
        return LPAnd(self, other)

    def __or__(self, other):
        return LPOr(self, other)

    def __not__(self):
        return LPNot(self)


class LPAnd(LinePred):
    def __init__(self, lp1, lp2):
        assert isinstance(lp1, LinePred)
        assert isinstance(lp2, LinePred)
        self.lp1 = lp1
        self.lp2 = lp2

    def test(self, line):
        return self.lp1.test(line) and self.lp2.test(line)


class LPOr(LinePred):
    def __init__(self, lp1, lp2):
        assert isinstance(lp1, LinePred)
        assert isinstance(lp2, LinePred)
        self.lp1 = lp1
        self.lp2 = lp2

    def test(self, line):
        return self.lp1.test(line) or self.lp2.test(line)


class LPNot(LinePred):
    def __init__(self, lp0):
        assert isinstance(lp0, LinePred)
        self.lp0 = lp0

    def test(self, line):
        return not self.lp0.test(line)


class LPTag(LinePred):
    def __init__(self, tag):
        assert isinstance(tag, (str, unicode))
        self.tag = tag

    def test(self, line):
        return line.tag == self.tag


class LPWanted(LinePred):
    """black-list rule"""
    def __init__(self, ifany):
        for lp in ifany:
            assert isinstance(lp, LinePred)
        self.ifany = ifany

    def test(self, line):
        for lp in ifany:
            if lp.test(line):
                return True
        return False


class LPBanned(LinePred):
    """white-list rule"""
    def __init__(self, ifany):
        for lp in ifany:
            assert isinstance(lp, LinePred)
        self.ifany = ifany

    def test(self, line):
        for lp in self.ifany:
            if lp.test(line):
                return False
        return True

