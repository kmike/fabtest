#!/usr/bin/env python
import sys
import unittest
from fabric.api import run
from fabtest import FabTest, fab

def whoami():
    return run('whoami')

class MyTestCase(FabTest):
    def test_root_login(self):
        output = fab(whoami)
        self.assertEqual(output[0], 'root')

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
