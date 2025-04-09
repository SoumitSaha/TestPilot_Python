import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_1(self):
        result = emoji.emoji_list("Hello World! 🌍")
        expected = [{'match_start': 12, 'match_end': 13, 'emoji': '🌍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_2(self):
        result = emoji.emoji_list("No emoji here.")
        expected = []
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_3(self):
        result = emoji.emoji_list("Multiple emojis 👍👍")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '👍'}, {'match_start': 16, 'match_end': 17, 'emoji': '👍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_4(self):
        result = emoji.emoji_list("Emoji at start 🎉 of the string.")
        expected = [{'match_start': 0, 'match_end': 1, 'emoji': '🎉'}]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
    
#End of Code