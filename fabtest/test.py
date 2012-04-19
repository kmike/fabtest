import unittest
import time
import platform

from fabric.api import env
from fabric import state
from fabric.network import disconnect_all

from fabtest.vbox import VirtualBox
from fabtest.utils import force_ssh_reconnect

class VirtualBoxTest(unittest.TestCase):
    vm_name = 'Squeeze' # name or uuid of VirtualBox VM
    vbox_command = 'VBoxManage'  # command to execute VBoxManage
    snapshot = 'fabtest-initial' # snapshot to load before each test
    keep_box = False # don't stop the VM after tests; useful for manual investigation

    # set this to False if snapshots are taken during tests
    # or if you want to be able to login to VM in a separate shell
    headless = True

    def setUp(self):
        self._snapshots = []
        self.box = VirtualBox(self.vm_name, self.vbox_command)
        self.activate_snapshot(self.snapshot)

    def tearDown(self):
        if self.keep_box:
            return
        self.box.stop()
        for name in self._snapshots:
            self.box.snapshot('delete', name)

    def activate_snapshot(self, name):
        if platform.system()=='Windows':
            RETRIES_CNT = 5
            for i in xrange(RETRIES_CNT):
                if self.box.snapshot_exists(name):
           	        break
                else:
                    time.sleep(1)
        assert self.box.snapshot_exists(name), 'Snapshot "%s" does not exist' % name
        self.box.stop()
        self.box.snapshot('restore', name)
        self.box.start(self.headless)

    def take_test_snapshot(self, name):
        """
        Creates temporary snapshot that will be deleted after test.
        """
        self._snapshots.append(name)
        self.box.snapshot_take(name)


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
        env.timeout = 1 # local virtualbox connections should be fast
        env.disable_known_hosts = True

    def take_test_snapshot(self, name, reconnect=True):
        super(FabTest, self).take_test_snapshot(name)
        if reconnect:
            force_ssh_reconnect()

    def activate_test_snapshot(self, name, reconnect=True):
        """
        Activates test snapshot.
        """
        self.activate_snapshot(name)
        if reconnect:
            force_ssh_reconnect()
