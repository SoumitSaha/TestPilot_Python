import emoji
import unittest

class TestemojiModule(unittest.TestCase):
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
#End of Code