import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    # ========== Test for emoji_demojize base =============
    def test_emoji_demojize_0(self):
        result = emoji.demojize("I love 🍕!")
        self.assertEqual(result, "I love :pizza:!")

    def test_emoji_demojize_1(self):
        result = emoji.demojize("Hello 👋", delimiters=("~", "~"))
        self.assertEqual(result, "Hello ~waving_hand~")

    def test_emoji_demojize_2(self):
        result = emoji.demojize("Python is awesome 🐍💻", language="en")
        self.assertEqual(result, "Python is awesome :snake::laptop:")

    def test_emoji_demojize_3(self):
        result = emoji.demojize("Good morning ☀️", version=1.0)
        self.assertEqual(result, "Good morning :sun:")

    def test_emoji_demojize_4(self):
        result = emoji.demojize("I am happy 😀", handle_version=None)
        self.assertEqual(result, "I am happy :grinning_face:")

    #func_body
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

    #example
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

    #docstring
    def test_emoji_demojize_docstring_0(self):
        result = emoji.demojize("Python is fun 👍")
        expected = "Python is fun :thumbs_up:"
        self.assertEqual(result, expected)

    def test_emoji_demojize_docstring_1(self):
        result = emoji.demojize("Python is fun 👍", delimiters=("__", "__"))
        expected = "Python is fun __thumbs_up__"
        self.assertEqual(result, expected)

    def test_emoji_demojize_docstring_2(self):
        result = emoji.demojize("Python is fun 👍", language='es')
        expected = "Python is fun :pulgar_hacia_arriba:"
        self.assertEqual(result, expected)

    def test_emoji_demojize_docstring_3(self):
        result = emoji.demojize("Python is fun 🔥")
        expected = "Python is fun :fire:"
        self.assertEqual(result, expected)

    def test_emoji_demojize_docstring_4(self):
        def replace_emoji(emj, data):
            return data['alias'][0] if data['E'] > 1.0 else emj
        result = emoji.demojize("Python is fun 🔥", handle_version=replace_emoji)
        expected = "Python is fun :fire:"  # This emoji is in version 1.0, so it should be replaced by the alias
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
