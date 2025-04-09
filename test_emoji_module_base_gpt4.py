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

if __name__ == '__main__':
    unittest.main()
