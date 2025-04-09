import emoji
import unittest

class TestemojiModule(unittest.TestCase):

    def test_emoji_demojize_example_0(self):
        result = emoji.demojize("Python is fun 👍")
        self.assertEqual(result, "Python is fun :thumbs_up:")

    def test_emoji_demojize_example_1(self):
        result = emoji.demojize("icode is tricky 😯", delimiters=("__", "__"))
        self.assertEqual(result, "icode is tricky __hushed_face__")

    def test_emoji_demojize_example_2(self):
        result = emoji.demojize("I love 🍕 and 🍔")
        self.assertEqual(result, "I love :pizza: and :hamburger:")

    def test_emoji_demojize_example_3(self):
        result = emoji.demojize("It's ☔ today", language='en')
        self.assertEqual(result, "It's :umbrella_with_rain_drops: today")

    def test_emoji_demojize_example_4(self):
        result = emoji.demojize("🤓 coding in Python is fun", version=1.0, delimiters=("__", "__"))
        self.assertEqual(result, "__nerd_face__ coding in Python is fun")


if __name__ == '__main__':
    unittest.main()
    
#End of Code