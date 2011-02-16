from fabric import state
from fabric.main import get_hosts
from fabric.network import interpret_host_string, HostConnectionCache

def fab(command, *args, **kwargs):
    """ Runs fab command. Accepts callable. """

    # clean the connection cache
    state.connections = HostConnectionCache()

    # partially implement the logic from fabric.main.main
    state.env.command = command.__name__
    state.env.all_hosts = hosts = get_hosts(command, None, None)
    for host in hosts:
        interpret_host_string(host)
        command(*args, **kwargs)

