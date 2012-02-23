# -*- coding: utf-8 -*-
import fudge
import unittest

from example import sorted_numbers

class Test(unittest.TestCase):

    @fudge.patch('example.sorted_ci')
    def test_with_fudge(self, sorted_ci):
        sorted_ci.expects_call().returns(('4', '5'))
        assert sorted_numbers((5, 4)) == ('4', '5')

if __name__ == '__main__':
    unittest.main()

