=======
Fabtest
=======

Fabtest is a set of utilities and base TestCases that aid testing Fabric
scripts against VirtualBox VMs. License is MIT.

VM is rolled back to initial state before each test so tests can do anything
with target system; Fabric commands can be run from Python.

Installation
------------

::

    pip install fabtest

VMs
---

In order to run tests you'll need `VirtualBox`_ 4.x and an OS image.
Image should have ssh server installed.

.. note::

    Example VMs:

    * `Lenny.ova (312M) <http://dl.dropbox.com/u/21197464/Lenny.ova>`_
    * `Squeeze.ova (436M) <http://dl.dropbox.com/u/21197464/Squeeze.ova>`_
    * `Ubuntu-10.10.ova (277M) <http://dl.dropbox.com/u/21197464/Ubuntu-10.10.ova>`_

After you get the image, make sure it is not running and execute the
``fabtest-preparevm`` script (pass your VM name or uid to it)::

    fabtest-preparevm Lenny

This command configures port forwarding (127.0.0.1:2222 to guest 22 port,
127.0.0.1:8888 to guest 80 port) and takes 'fabtest-initial' snapshot
used for test rollbacks (it is taken from booted machine in order to
speedup tests).

.. _VirtualBox: http://www.virtualbox.org/

Writing tests
-------------

Subclass fabtest.VirtualBoxTest or fabtest.FabTest and use fabtest.fab for
fabric commands execution::

    from fabric.api import run
    from fabtest import FabTest, fab

    class MyTestCase(FabTest):

        def test_root_login(self):
            def fabric_command():
                output = run('whoami')
                self.assertEqual(output, 'root')
            fab(fabric_command)

Look at source code (and example/runtests.py) for more.
