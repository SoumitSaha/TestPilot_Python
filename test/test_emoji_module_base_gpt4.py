import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    # ========== Test for emoji_demojize =============
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

    # ========== Test for emoji_core_demojize =============
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
