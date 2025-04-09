import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_demojize_example_0(self):
        result = emoji.core.demojize("Python is fun 👍")
        self.assertEqual(result, "Python is fun :thumbs_up:")

    def test_emoji_core_demojize_example_1(self):
        result = emoji.core.demojize("icode is tricky 😯", delimiters=("__", "__"))
        self.assertEqual(result, "icode is tricky __hushed_face__")

    def test_emoji_core_demojize_example_2(self):
        result = emoji.core.demojize("I love Python ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love Python :red_heart:")

    def test_emoji_core_demojize_example_3(self):
        result = emoji.core.demojize("Good job 🎉", language='en')
        self.assertEqual(result, "Good job :party_popper:")

    def test_emoji_core_demojize_example_4(self):
        result = emoji.core.demojize("Let's eat 🍕", handle_version=None)
        self.assertEqual(result, "Let's eat :pizza:")

if __name__ == '__main__':
    unittest.main()

#End of Code
