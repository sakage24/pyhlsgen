from .movie import Source
from .movie import Manager
import os
import unittest


class TestRun(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.removedirs('c:\\users\\aaaok\\Desktop\\testCreated')
        except OSError:
            pass

    def test_get_media_list(self):
        Source.SOURCE_FILE_DIRECTORY._value_ = 'd:\\AV'
        manager = Manager()
        self.assertTrue(manager.get_movie_list())
        for i in manager.get_movie_list():
            print(i)

    def test_makedir(self):
        Source.DESTINATION_FILE_DIRECTORY._value_ = 'c:\\Users\\aaaok\\Desktop\\testCreated'
        manager = Manager()
        self.assertTrue(manager.make_directory(Source.DESTINATION_FILE_DIRECTORY.value))

    def test_replace_character(self):
        manager = Manager()
        word = 'abcdefgあいうえお.mp4'
        expected_word = 'abcdefg_____.mp4'
        result = manager.get_replace_character(word)
        self.assertEqual(result, expected_word)
        print(result, expected_word)

if __name__ == '__main__':
    unittest.main()
