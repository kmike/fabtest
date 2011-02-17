import unittest
from fabtest.vbox import VirtualBox
from fabric.api import env, run
from fabric.state import _AttributeDict

class VirtualBoxTest(unittest.TestCase):
    vm_name = 'Squeeze'
    vbox_command = 'VBoxManage'
    snapshot = 'fabtest-initial'

    # set this to False if snapshots are taken during tests
    # or if you want to be able to login to VM in a separate shell
    headless = True

    def setUp(self):
        self.box = VirtualBox(self.vm_name, self.vbox_command)
        self.activate_snapshot(self.snapshot)

    def tearDown(self):
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
        super(FabTest, self).setUp()
        self.previous_env = _AttributeDict(env)
        self.setup_env()

    def tearDown(self):
        env.update(self.previous_env)
        super(FabTest, self).tearDown()

    def setup_env(self):
        env.hosts = [self.host]
        env.password = self.password
        env.key_filename = self.key_filename
        env.disable_known_hosts = True

