import subprocess
from functools import partial
import urllib2

class VirtualBox(object):
    """
    Simplest VirtualBox connection class.
    Its attributes are converted to a functions calling
    VBoxManage shell command, e.g. this::

        box = VirtualBox('MyVM')
        box.startvm('--type', 'headless')

    will execute this::

        VBoxManage startvm MyVM --type headless

    Positional args are used to build VBoxManage command,
    kwargs are passed to subprocess.call.

    Please read VBoxManage reference manual for more info.
    """

    def __init__(self, name, vbox_command='VBoxManage'):
        self.name = name
        self.vbox_command = vbox_command

    def __getattr__(self, name):
        return partial(self, name)

    def __call__(self, command, *args, **kwargs):
        params = [self.vbox_command, command, self.name] + list(args)
        print '$ ' + ' '.join(params)
        return subprocess.call(params, **kwargs)

    # some common wrappers
    def start(self, headless=False):
        # headless variant leads to invalid snapshots for some reason
        # (bug in virtualbox?)
        if headless:
            self.startvm('--type', 'headless')
        else:
            self.startvm()

    def stop(self, ignore_errors=True):
        stderr = subprocess.PIPE if ignore_errors else None
        self.controlvm('poweroff', stderr=stderr)

    def snapshot_exists(self, name):
        res = self.snapshot('showvminfo', name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res == 0

    def snapshot_take(self, name, *args, **kwargs):
        """
        Takes snapshot. Without pause/resume VirtualBox fails with
        VERR_SSM_LIVE_GURU_MEDITATION.
        """
        self.controlvm('pause')
        result = self.snapshot('take', name, *args, **kwargs)
        self.controlvm('resume')
        return result

    def snapshot_restore(self, name):
        self.stop()
        self.snapshot('restore', name)
        self.start()



def vbox_urlopen(fullurl, data=None, vbox_http = '127.0.0.1:8888'):
    """
    Wrapper for performing http requests to VM. The trick is to
    treat VM as a proxy.

    This::

        vbox_urlopen('http://example.com')

    removes the need to do this:

        1. add '127.0.0.1 example.com' line to ``hosts`` file
        2. call urllib2.urlopen('http://example.com:8888')
        3. remove '127.0.0.1 example.com' from hosts
    """
    proxy_handler = urllib2.ProxyHandler({'http': vbox_http})
    opener = urllib2.build_opener(proxy_handler)
    return opener.open(fullurl, data)
