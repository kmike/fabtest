#!/usr/bin/env python
import sys
import unittest
from fabric.api import run
from fabric.contrib.files import exists
from fabtest import FabTest, fab

def whoami():
    return run('whoami')

class MyTestCase(FabTest):
    def test_root_login(self):
        self.assertEqual(fab(whoami), 'root')

    def test_snapshots(self):

        test_file = '~/test_file.tmp'
        def mkfile():
            return run('touch '+test_file)

        def file_exists():
            return exists(test_file)

        self.assertFalse(fab(file_exists))
        fab(mkfile)
        self.assertTrue(fab(file_exists))

        self.take_test_snapshot('test-snapshot')
        self.assertTrue(fab(file_exists))

        self.activate_test_snapshot(self.snapshot)
        self.assertFalse(fab(file_exists))

        self.activate_test_snapshot('test-snapshot')
        self.assertTrue(fab(file_exists))


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
