import subprocess
from functools import partial

class VirtualBox(object):
    def __init__(self, name, vbox_command='VBoxManage'):
        self.name = name
        self.vbox_command = vbox_command

    def __getattr__(self, name):
        """
        Attributes are converted to a functions calling
        VBoxManage shell command.
        """
        return partial(self, name)

    def __call__(self, command, *args, **kwargs):
        params = [self.vbox_command, command, self.name] + list(args)
        print '$ ' + ' '.join(params)
        return subprocess.call(params, **kwargs)

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
        res = self.snapshot('showvminfo', name, stdout=subprocess.PIPE)
        return res == 0
