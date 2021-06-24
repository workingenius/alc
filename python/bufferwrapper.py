import vim

from analyze import Analyzed, analyze

buffer_type = type(vim.current.buffer)


# When buffer objects as key, buf.number is set as real key

# Each "original" buffer has two auxilary buffer, "view" and "conf"

# origin buffer to Analyzed object
_origin_to_analyzed = {}

# origins 
_buffer_to_origin = {}

# views
_buffer_to_view = {}

# confs
_buffer_to_conf = {}


class BufferWrapper(object):
    def __init__(self, buffer):
        assert isinstance(buffer, buffer_type)
        self.buffer = buffer
        self.num = buffer.number

    @property
    def is_prepared(self):
        if self.num in _buffer_to_origin:
            assert self.num in _buffer_to_view
            assert self.num in _buffer_to_conf
            return True
        else:
            assert self.num not in _buffer_to_view
            assert self.num not in _buffer_to_conf
            return False

    def prepare(self):
        assert not self.is_prepared
        # assume that the current is origin, and loaded
        name = self.buffer.name
        analyzed = analyze(self.buffer)
        contents = list(vim.current.buffer)

        # create a new buffer as view, and copy contents from origin to here
        vim.command(':enew')
        view_buffer = vim.current.buffer
        view_buffer.name = name + '.viewbuf'
        vim.current.buffer[:] = contents
        del contents

        # create a new buffer as conf, empty by default
        vim.command(':enew')
        conf_buffer = vim.current.buffer
        conf_buffer.name = name + '.confbuf'

        # register buffers
        origin_num = self.num
        view_num = view_buffer.number
        conf_num = conf_buffer.number
        _buffer_to_origin[origin_num] = origin_num
        _buffer_to_origin[view_num] = origin_num
        _buffer_to_origin[conf_num] = origin_num
        _buffer_to_view[origin_num] = view_num
        _buffer_to_view[view_num] = view_num
        _buffer_to_view[conf_num] = view_num
        _buffer_to_conf[origin_num] = conf_num
        _buffer_to_conf[view_num] = conf_num
        _buffer_to_conf[conf_num] = conf_num
        # register analyzed object
        _origin_to_analyzed[origin_num] = analyzed

        # Show view buffer
        vim.command(':b ' + str(view_num))

    @property
    def analyzed(self):
        return _origin_to_analyzed.get(self.origin_buf.buffer.number)

    @property
    def is_view_buf(self):
        return _buffer_to_view.get(self.num) == self.num

    @property
    def is_conf_buf(self):
        return _buffer_to_conf.get(self.num) == self.num

    @property
    def is_origin_buf(self):
        return _buffer_to_origin.get(self.num) == self.num

    @property
    def origin_buf(self):
        return BufferWrapper(vim.buffers[_buffer_to_origin.get(self.num)])

    @property
    def view_buf(self):
        return BufferWrapper(vim.buffers[_buffer_to_view.get(self.num)])

    @property
    def conf_buf(self):
        return BufferWrapper(vim.buffers[_buffer_to_conf.get(self.num)])

    @classmethod
    def current(self):
        return BufferWrapper(vim.current.buffer)

    @classmethod
    def get(self, number):
        return BufferWrapper(vim.buffers[number])

    def __eq__(self, other):
        return self.buffer.number == other.buffer.number

