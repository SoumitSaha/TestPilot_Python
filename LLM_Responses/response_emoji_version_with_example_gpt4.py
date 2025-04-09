import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_version_example_0(self):
        result = emoji.version("😁")
        self.assertIsInstance(result, float)

    def test_emoji_version_example_1(self):
        result = emoji.version(":butterfly:")
        self.assertIsInstance(result, int)

    def test_emoji_version_example_2(self):
        result = emoji.version(":smile:")
        self.assertIsInstance(result, float)

    def test_emoji_version_example_3(self):
        result = emoji.version(":grin:")
        self.assertIsInstance(result, float)

    def test_emoji_version_example_4(self):
        result = emoji.version(":laughing:")
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()
#End of Code