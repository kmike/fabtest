#!/usr/bin/env python
import sys
import unittest
from fabric.api import run
from fabric.contrib.files import exists
from fabtest import FabTest, fab

def whoami():
    return run('whoami')

def mkfile():
    return run('touch ~/file-exists')

class MyTestCase(FabTest):
    def test_root_login(self):
        output = fab(whoami)
        self.assertEqual(output[0], 'root')

    def test_snapshots(self):

        test_file = '~/test_file.tmp'
        def mkfile():
            return run('touch '+test_file)

        def file_exists():
            return exists(test_file)

        self.assertFalse(fab(file_exists)[0])
        fab(mkfile)
        self.assertTrue(fab(file_exists)[0])

        self.take_snapshot('test-snapshot')
        self.assertTrue(fab(file_exists)[0])

        self.activate_snapshot(self.snapshot)
        self.assertFalse(fab(file_exists)[0])

        self.activate_snapshot('test-snapshot')
        self.assertTrue(fab(file_exists)[0])


def help():
    print 'usage: ./runtests.py "VM NAME"'
    print 'VM should be prepared with fabtest-preparevm script,'
    print 'root password must be 123.'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        help()
    else:
        MyTestCase.vm_name = sys.argv[1]
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        unittest.main()
