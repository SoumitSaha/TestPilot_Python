import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_demojize_0(self):
        result = emoji.core.demojize("Hello 😊")
        self.assertEqual(result, "Hello :smiling_face_with_smiling_eyes:")

    def test_emoji_core_demojize_1(self):
        result = emoji.core.demojize("I love coding ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love coding :red_heart:")

    def test_emoji_core_demojize_2(self):
        result = emoji.core.demojize("Let's party 🎉🎊", delimiters=(':', ':'), language='en')
        self.assertEqual(result, "Let's party :party_popper::confetti_ball:")

    def test_emoji_core_demojize_3(self):
        result = emoji.core.demojize("Python is awesome 🐍", version=3.0)
        self.assertEqual(result, "Python is awesome :snake:")

    def test_emoji_core_demojize_4(self):
        result = emoji.core.demojize("Good morning 🌞", handle_version=None)
        self.assertEqual(result, "Good morning :sun_with_face:")

    def test_emoji_core_demojize_docstring_0(self):
        result = emoji.core.demojize("Python is fun 👍")
        self.assertEqual(result, "Python is fun :thumbs_up:")

    def test_emoji_core_demojize_docstring_1(self):
        result = emoji.core.demojize("icode is tricky 😯", delimiters=("__", "__"))
        self.assertEqual(result, "icode is tricky __hushed_face__")

    def test_emoji_core_demojize_docstring_2(self):
        result = emoji.core.demojize("I love Python ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love Python :red_heart:")

    def test_emoji_core_demojize_docstring_3(self):
        result = emoji.core.demojize("Good job 🎉", language='en')
        self.assertEqual(result, "Good job :party_popper:")

    def test_emoji_core_demojize_docstring_4(self):
        result = emoji.core.demojize("Let's eat 🍕", handle_version=None)
        self.assertEqual(result, "Let's eat :pizza:")

    def test_emoji_core_demojize_funcBody_0(self):
        result = emoji.core.demojize("I love programming ❤️")
        self.assertEqual(result, "I love programming :red_heart:")

    def test_emoji_core_demojize_funcBody_1(self):
        result = emoji.core.demojize("Good morning 🌞", delimiters=('__', '__'))
        self.assertEqual(result, "Good morning __sun_with_face__")

    def test_emoji_core_demojize_funcBody_2(self):
        result = emoji.core.demojize("Python is fun 👍", language='es')
        self.assertEqual(result, "Python is fun :pulgar_hacia_arriba:")

    def test_emoji_core_demojize_funcBody_3(self):
        result = emoji.core.demojize("Let's party 🎉🎊", version=3.0)
        self.assertEqual(result, "Let's party :party_popper::confetti_ball:")

    def test_emoji_core_demojize_funcBody_4(self):
        result = emoji.core.demojize("Amazing! 😍", handle_version=':smiling_face_with_heart-eyes:')
        self.assertEqual(result, "Amazing! :smiling_face_with_heart-eyes:")

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
