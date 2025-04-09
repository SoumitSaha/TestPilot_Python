import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_version_docstring_0(self):
        result = emoji.version("😁")
        self.assertEqual(result, 0.6)

    def test_emoji_version_docstring_1(self):
        result = emoji.version(":butterfly:")
        self.assertEqual(result, 3)

    def test_emoji_version_docstring_2(self):
        with self.assertRaises(ValueError):
            emoji.version("This is a string without any emoji")

    def test_emoji_version_docstring_3(self):
        result = emoji.version(":smile:")
        # Assuming version for :smile: emoji is 0.6
        self.assertEqual(result, 0.6)

    def test_emoji_version_docstring_4(self):
        result = emoji.version("🐶")
        # Assuming version for 🐶 emoji is 0.6
        self.assertEqual(result, 0.6)

if __name__ == '__main__':
    unittest.main()

#End of Code