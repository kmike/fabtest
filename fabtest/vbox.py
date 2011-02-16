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

    def __call__(self, command, *args):
        params = [self.vbox_command, command, self.name] + list(args)
        print '$ ' + ' '.join(params)
        return subprocess.call(params)

    def start(self):
        # headless variant leads to invalid snapshots for some reason
        # (bug in virtualbox?)
        # self.startvm('--type', 'headless')
        self.startvm()

    def stop(self):
        self.controlvm('poweroff')

    def snapshot_exists(self, name):
        res = self.snapshot('showvminfo', name)
        return res == 0
