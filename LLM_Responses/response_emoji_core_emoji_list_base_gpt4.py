import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0(self):
        # Write code to test the emoji.core.emoji_list method
        result = emoji.emoji_list('')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_1(self):
        # Write code to test the emoji.core.emoji_list method
        result = emoji.emoji_list('Hello world!')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2(self):
        # Write code to test the emoji.core.emoji_list method
        result = emoji.emoji_list('Hello world! 😃')
        self.assertEqual(result, [{'location': 13, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_3(self):
        # Write code to test the emoji.core.emoji_list method
        result = emoji.emoji_list('😃😃😃')
        self.assertEqual(result, [{'location': 0, 'emoji': '😃'}, {'location': 1, 'emoji': '😃'}, {'location': 2, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_4(self):
        # Write code to test the emoji.core.emoji_list method
        result = emoji.emoji_list('Hello 😃 world! 😃😃')
        self.assertEqual(result, [{'location': 6, 'emoji': '😃'}, {'location': 14, 'emoji': '😃'}, {'location': 15, 'emoji': '😃'}])


if __name__ == '__main__':
    unittest.main()

#End of Code