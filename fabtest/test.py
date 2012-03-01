import unittest

from fabric.api import env
from fabric import state
from fabric.state import connections
from fabtest.utils import force_ssh_reconnect

from fabtest.vbox import VirtualBox
from fabric.network import disconnect_all

class VirtualBoxTest(unittest.TestCase):
    vm_name = 'Squeeze' # name or uuid of VirtualBox VM
    vbox_command = 'VBoxManage'  # command to execute VBoxManage
    snapshot = 'fabtest-initial' # snapshot to load before each test
    keep_box = False # don't stop the VM after tests; useful for manual investigation

    # set this to False if snapshots are taken during tests
    # or if you want to be able to login to VM in a separate shell
    headless = True

    def setUp(self):
        self.box = VirtualBox(self.vm_name, self.vbox_command)
        self.activate_snapshot(self.snapshot)

    def tearDown(self):
        if not self.keep_box:
            self.box.stop()

    def activate_snapshot(self, name):
        assert self.box.snapshot_exists(name), 'Snapshot "%s" does not exist' % name
        self.box.stop()
        self.box.snapshot('restore', name)
        self.box.start(self.headless)


class FabTest(VirtualBoxTest):
    host = 'root@127.0.0.1:2222'
    password = '123'
    key_filename = None

    def setUp(self):
        self.setup_env()
        disconnect_all()
        self.previous_env = state._AttributeDict(env)
        super(FabTest, self).setUp()

    def tearDown(self):
        disconnect_all()
        env.update(self.previous_env)
        super(FabTest, self).tearDown()

    def setup_env(self):
        env.hosts = [self.host]
        env.password = self.password
        env.host_string = self.host
        env.key_filename = self.key_filename
        env.disable_known_hosts = True
