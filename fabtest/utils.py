from fabric import state
from fabric.main import get_hosts
from fabric.network import interpret_host_string

class FabricAbortException(Exception):
    pass

def fab(command, *args, **kwargs):
    """ Runs fab command. Accepts callable. """

    # collect results
    results = []

    # partially implement the logic from fabric.main.main
    state.env.command = command.__name__
    state.env.all_hosts = hosts = get_hosts(command, None, None)

    try: # convert fabric.abort() calls to real exceptions
        for host in hosts:
            interpret_host_string(host)
            res = command(*args, **kwargs)
            results.append(res)
        return results
    except SystemExit, e:
        import traceback
        traceback.print_exc()
        raise FabricAbortException()

def close_fabric_connections():
    for key, connection in state.connections.items():
        connection.close()
        del state.connections[key]


