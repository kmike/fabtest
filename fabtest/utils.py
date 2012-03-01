from __future__ import absolute_import
import functools
from fabric.api import env
from fabric.state import connections
from fabric.tasks import execute

class FabricAbortException(Exception):
    pass

def catch_aborts(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SystemExit, e:
            import traceback
            traceback.print_exc()
            tb = traceback.format_exc()
            raise FabricAbortException(tb)
    return inner

execute_safe = catch_aborts(execute)
execute_safe.__doc__ = """
Runs fab command. Similar to fabric.task.execute but
converts 'abort' calls to exceptions of type FabricAbortException.
"""

def fab(command, *args, **kwargs):
    """
    Runs fab command. Similar to fabric.task.execute but
    converts 'abort' calls to exceptions of type FabricAbortException
    and returns a single result, not a dictionary. This is convenient
    when there is only a single host.
    """
    return execute_safe(command, *args, **kwargs).values()[0]


def force_ssh_reconnect():
    connections.connect(env.host_string)