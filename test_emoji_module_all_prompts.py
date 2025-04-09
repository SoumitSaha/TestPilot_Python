import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_demojize_0_base(self):
        result = emoji.core.demojize("Hello 😊")
        self.assertEqual(result, "Hello :smiling_face_with_smiling_eyes:")

    def test_emoji_core_demojize_1_base(self):
        result = emoji.core.demojize("I love coding ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love coding :red_heart:")

    def test_emoji_core_demojize_2_base(self):
        result = emoji.core.demojize("Let's party 🎉🎊", delimiters=(':', ':'), language='en')
        self.assertEqual(result, "Let's party :party_popper::confetti_ball:")

    def test_emoji_core_demojize_3_base(self):
        result = emoji.core.demojize("Python is awesome 🐍", version=3.0)
        self.assertEqual(result, "Python is awesome :snake:")

    def test_emoji_core_demojize_4_base(self):
        result = emoji.core.demojize("Good morning 🌞", handle_version=None)
        self.assertEqual(result, "Good morning :sun_with_face:")

    def test_emoji_core_demojize_0_docstring(self):
        result = emoji.core.demojize("Python is fun 👍")
        self.assertEqual(result, "Python is fun :thumbs_up:")

    def test_emoji_core_demojize_1_docstring(self):
        result = emoji.core.demojize("icode is tricky 😯", delimiters=("__", "__"))
        self.assertEqual(result, "icode is tricky __hushed_face__")

    def test_emoji_core_demojize_2_docstring(self):
        result = emoji.core.demojize("I love Python ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love Python :red_heart:")

    def test_emoji_core_demojize_3_docstring(self):
        result = emoji.core.demojize("Good job 🎉", language='en')
        self.assertEqual(result, "Good job :party_popper:")

    def test_emoji_core_demojize_4_docstring(self):
        result = emoji.core.demojize("Let's eat 🍕", handle_version=None)
        self.assertEqual(result, "Let's eat :pizza:")

    def test_emoji_core_demojize_0_body(self):
        result = emoji.core.demojize("I love programming ❤️")
        self.assertEqual(result, "I love programming :red_heart:")

    def test_emoji_core_demojize_1_body(self):
        result = emoji.core.demojize("Good morning 🌞", delimiters=('__', '__'))
        self.assertEqual(result, "Good morning __sun_with_face__")

    def test_emoji_core_demojize_2_body(self):
        result = emoji.core.demojize("Python is fun 👍", language='es')
        self.assertEqual(result, "Python is fun :pulgar_hacia_arriba:")

    def test_emoji_core_demojize_3_body(self):
        result = emoji.core.demojize("Let's party 🎉🎊", version=3.0)
        self.assertEqual(result, "Let's party :party_popper::confetti_ball:")

    def test_emoji_core_demojize_4_body(self):
        result = emoji.core.demojize("Amazing! 😍", handle_version=':smiling_face_with_heart-eyes:')
        self.assertEqual(result, "Amazing! :smiling_face_with_heart-eyes:")

    def test_emoji_core_demojize_0_example(self):
        result = emoji.core.demojize("Python is fun 👍")
        self.assertEqual(result, "Python is fun :thumbs_up:")

    def test_emoji_core_demojize_1_example(self):
        result = emoji.core.demojize("icode is tricky 😯", delimiters=("__", "__"))
        self.assertEqual(result, "icode is tricky __hushed_face__")

    def test_emoji_core_demojize_2_example(self):
        result = emoji.core.demojize("I love Python ❤️", delimiters=(':', ':'))
        self.assertEqual(result, "I love Python :red_heart:")

    def test_emoji_core_demojize_3_example(self):
        result = emoji.core.demojize("Good job 🎉", language='en')
        self.assertEqual(result, "Good job :party_popper:")

    def test_emoji_core_demojize_4_example(self):
        result = emoji.core.demojize("Let's eat 🍕", handle_version=None)
        self.assertEqual(result, "Let's eat :pizza:")

if __name__ == '__main__':
    unittest.main()
