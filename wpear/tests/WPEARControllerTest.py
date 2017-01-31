#!/usr/bin/env python

import unittest
import sys
sys.path.insert(0, '../')

import WPEARController

class WPEARControllerTestCase(unittest.TestCase):

    def testStartRun(self):
        WPEARController.StartRun()

if __name__ == '__main__':
    unittest.main()
