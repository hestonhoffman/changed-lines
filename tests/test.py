'''
Tests for the main.py file
'''
import unittest
import sys
import test_data

# sys.path.append('../')

from main import (
    parse_patch_data,
    get_lines
) # pylint: disable=wrong-import-position

class TestParsePatchData(unittest.TestCase):
    '''Test the parse_patch_data function'''
    unittest.TestCase.maxDiff = None
    def test_removed(self):
        '''status['removed'] returns empty value'''
        given = test_data.STATUS_REMOVED
        got = parse_patch_data(given)
        want = {}
        self.assertEqual(got, want)

    def test_modified(self):
        '''status['modified'] returns a dictionary of files and the lines'''
        given = test_data.STATUS_MODIFIED
        got = parse_patch_data(given)
        want = test_data.TEST_MODIFIED_ANSWER
        self.assertEqual(got, want)

    def test_no_patch(self):
        '''missing patch key returns empty value'''
        given = test_data.STATUS_NO_PATCH
        got = parse_patch_data(given)
        want = {}
        self.assertEqual(got, want)

class TestGetLines(unittest.TestCase):
    '''Test the get_lines function'''
    def test_get_lines(self):
        '''Returns the correct line numbers for each file'''
        given = test_data.TEST_MODIFIED_ANSWER
        got = get_lines(given)
        want = test_data.TEST_GET_LINES_ANSWER
        self.assertEqual(got, want)

if __name__ == '__main__':
    unittest.main()
