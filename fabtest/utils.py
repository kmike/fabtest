from __future__ import absolute_import
from fabric.api import env
from fabric.state import connections
from fabric.tasks import execute

class FabricAbortException(Exception):
    pass

def fab(command, *args, **kwargs):
    """
    Runs fab command. Similar to fabric.task.execute but
    converts 'abort' calls to exceptions of type FabricAbortException
    and returns a list of results, not a dictionary.
    """
    try:
        results = execute(command, *args, **kwargs)
        # .values() is for backward compatibility with fabtest 0.0.8
        # XXX: do we need backward compatibility?
        return results.values()
    except SystemExit, e:
        import traceback
        traceback.print_exc()
        raise FabricAbortException()

def force_ssh_reconnect():
    connections.connect(env.host_string)