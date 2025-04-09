import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_version_0(self):
        self.assertIsInstance(emoji.__version__, str)  # Assuming emoji.module returns a string value version

    def test_emoji_version_1(self):
        version = emoji.__version__.split('.')
        self.assertEqual(len(version), 3)  # Checking if the version is in the format x.y.z

    def test_emoji_version_2(self):
        version = emoji.__version__.split('.')
        self.assertTrue(version[0].isdigit())  # Checking if major version is a number

    def test_emoji_version_3(self):
        version = emoji.__version__.split('.')
        self.assertTrue(version[1].isdigit())  # Checking if minor version is a number

    def test_emoji_version_4(self):
        version = emoji.__version__.split('.')
        self.assertTrue(version[2].isdigit())  # Checking if patch version is a number


if __name__ == '__main__':
    unittest.main()

#End of Code