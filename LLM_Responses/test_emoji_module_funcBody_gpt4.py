import emoji
import unittest

class TestemojiModule(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()

#End of Code
