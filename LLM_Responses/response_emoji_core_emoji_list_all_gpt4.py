import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0_base(self):
        result = emoji.emoji_list('')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_1_base(self):
        result = emoji.emoji_list('Hello world!')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2_base(self):
        result = emoji.emoji_list('Hello world! 😃')
        self.assertEqual(result, [{'match_start': 13, 'match_end': 14, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_3_base(self):
        result = emoji.emoji_list('😃😃😃')
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😃'}, {'match_start': 1, 'match_end': 2, 'emoji': '😃'}, {'match_start': 2, 'match_end': 3, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_4_base(self):
        result = emoji.emoji_list('Hello 😃 world! 😃😃')
        self.assertEqual(result, [{'match_start': 6, 'match_end': 7, 'emoji': '😃'}, {'match_start': 15, 'match_end': 16, 'emoji': '😃'}, {'match_start': 16, 'match_end': 17, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_0_func_body(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_1_func_body(self):
        result = emoji.emoji_list("Hello World! 🌍")
        expected = [{'match_start': 13, 'match_end': 14, 'emoji': '🌍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_2_func_body(self):
        result = emoji.emoji_list("No emoji here.")
        expected = []
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_3_func_body(self):
        result = emoji.emoji_list("Multiple emojis 👍👍")
        expected = [{'match_start': 16, 'match_end': 17, 'emoji': '👍'}, {'match_start': 17, 'match_end': 18, 'emoji': '👍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_4_func_body(self):
        result = emoji.emoji_list("Emoji at start 🎉 of the string.")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '🎉'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_0_docstring(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_1_docstring(self):
        result = emoji.emoji_list("No emojis here")
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2_docstring(self):
        result = emoji.emoji_list("Multiple emojis 😁👍")
        self.assertEqual(result, [{'match_start': 16, 'match_end': 17, 'emoji': '😁'}, {'match_start': 17, 'match_end': 18, 'emoji': '👍'}])

    def test_emoji_core_emoji_list_3_docstring(self):
        result = emoji.emoji_list("😁 at the start")
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_4_docstring(self):
        result = emoji.emoji_list("end with emoji 👍")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '👍'}])


if __name__ == '__main__':
    unittest.main()

#End of Code