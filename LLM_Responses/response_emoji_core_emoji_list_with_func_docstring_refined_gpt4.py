import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_1(self):
        result = emoji.emoji_list("No emojis here")
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2(self):
        result = emoji.emoji_list("Multiple emojis 😁👍")
        self.assertEqual(result, [{'match_start': 16, 'match_end': 17, 'emoji': '😁'}, {'match_start': 17, 'match_end': 18, 'emoji': '👍'}])

    def test_emoji_core_emoji_list_3(self):
        result = emoji.emoji_list("😁 at the start")
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_4(self):
        result = emoji.emoji_list("end with emoji 👍")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '👍'}])

if __name__ == '__main__':
    unittest.main()

# End of Code