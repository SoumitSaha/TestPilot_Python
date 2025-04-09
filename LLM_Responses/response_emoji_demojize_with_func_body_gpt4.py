import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_demojize_funcBody_0(self):
        result = emoji.demojize("Hello 👍")
        self.assertEqual(result, "Hello :thumbs_up:")

    def test_emoji_demojize_funcBody_1(self):
        result = emoji.demojize("Python is fun 🐍", delimiters=("__", "__"))
        self.assertEqual(result, "Python is fun __snake__")

    def test_emoji_demojize_funcBody_2(self):
        result = emoji.demojize("Python is fun 🐍", language = 'es')
        self.assertEqual(result, "Python is fun :serpiente:")

    def test_emoji_demojize_funcBody_3(self):
        result = emoji.demojize("Python is fun 🐍", language = 'de')
        self.assertEqual(result, "Python is fun :schlange:")

    def test_emoji_demojize_funcBody_4(self):
        result = emoji.demojize("Python is fun 🐍")
        self.assertEqual(result, "Python is fun :snake:")


if __name__ == '__main__':
    unittest.main()
#End of Code
