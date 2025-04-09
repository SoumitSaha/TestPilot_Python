import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0(self):
        result = emoji.emoji_list('')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_1(self):
        result = emoji.emoji_list('Hello world!')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2(self):
        result = emoji.emoji_list('Hello world! 😃')
        self.assertEqual(result, [{'match_start': 13, 'match_end': 14, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_3(self):
        result = emoji.emoji_list('😃😃😃')
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😃'}, {'match_start': 1, 'match_end': 2, 'emoji': '😃'}, {'match_start': 2, 'match_end': 3, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_4(self):
        result = emoji.emoji_list('Hello 😃 world! 😃😃')
        self.assertEqual(result, [{'match_start': 6, 'match_end': 7, 'emoji': '😃'}, {'match_start': 15, 'match_end': 16, 'emoji': '😃'}, {'match_start': 16, 'match_end': 17, 'emoji': '😃'}])

if __name__ == '__main__':
    unittest.main()

#End of Code