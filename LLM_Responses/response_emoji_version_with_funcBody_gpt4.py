import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_version_funcBody_0(self):
        # Test with emoji
        self.assertEqual(emoji.version("😁"), 0.6)
        
    def test_emoji_version_funcBody_1(self):
        # Test with emoji alias
        self.assertEqual(emoji.version(":butterfly:"), 3)

    def test_emoji_version_funcBody_2(self):
        # Test with string containing emoji
        self.assertEqual(emoji.version("Hello 😁"), 0.6)

    def test_emoji_version_funcBody_3(self):
        # Test with string containing emoji alias
        self.assertEqual(emoji.version("Hello :butterfly:"), 3)

    def test_emoji_version_funcBody_4(self):
        # Test with string without emoji, expect ValueError
        with self.assertRaises(ValueError):
            emoji.version("Hello World")


if __name__ == '__main__':
    unittest.main()

#End of Code