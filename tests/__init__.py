import unittest
from simpledict import Dictionary

class TestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_1(self):
        class Test(Dictionary): field_title = "t"; field_author = "a";
        minimized_data = {"t": "This is the title of the book 1", "a": "And the author 1"}
        normal_data = {"title": "This is the title of the book 2", "author": "And the author 2"}
        test_obj_from_minimized = Test(**minimized_data)
        assert('This is the title of the book 1' == test_obj_from_minimized['title'])
        assert(test_obj_from_minimized['t'] == 'This is the title of the book 1')
        assert(test_obj_from_minimized.title == 'This is the title of the book 1')
        test_obj_from_minimized['title'] = 'This is the ammended title of the book 1'
        assert(test_obj_from_minimized.title == 'This is the ammended title of the book 1')
        assert(test_obj_from_minimized['title'] == 'This is the ammended title of the book 1')
        assert(test_obj_from_minimized['t'] == 'This is the ammended title of the book 1')
        test_obj_from_minimized['t'] = 'This is the title of the book 1'
        assert(test_obj_from_minimized.title == 'This is the title of the book 1')
        assert(test_obj_from_minimized.author == 'And the author 1')
        test_obj_from_normal = Test(**normal_data)
        assert(test_obj_from_normal.title == 'This is the title of the book 2')
        assert(test_obj_from_normal.author == 'And the author 2')
        