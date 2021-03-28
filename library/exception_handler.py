from library.monitor.monitor import Monitor, BaseTags


class XCPBase(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(args)
        self._is_reported = False

    @property
    def is_reported(self):
        return self._is_reported

    @is_reported.setter
    def is_reported(self, value):
        self._is_reported = value

    @classmethod
    def get_inner_xcp(cls, xcp):
        def descend(top_item):
            if isinstance(top_item, tuple):
                for item in top_item:
                    return descend(item)
            elif issubclass(type(top_item), Exception):
                return top_item
            return None

        if hasattr(xcp, 'args'):
            for arg in xcp.args:
                return descend(arg)

    @classmethod
    def xcp_handler(cls, xcp: Exception, title: str = '', msg: str = '', tags: list = None):
        return cls.exception(title, xcp, msg, tags)

    @classmethod
    def exception(cls, title: str, e: Exception,  msg: str = '', tags: list = None):
        if isinstance(e, XCPBase):
            xcp = e
            if not xcp.is_reported:
                Monitor.exception(title, xcp, msg, tags)
                xcp.is_reported = True
        else:
            Monitor.exception(title, e, msg, tags)
            xcp = cls(e)
            xcp.is_reported = True
        return xcp


class GRequestFailed(RuntimeError):
    pass


class GRequest404(GRequestFailed):
    pass


class QBSvcErrNoQBAssign(RuntimeError):
    pass
