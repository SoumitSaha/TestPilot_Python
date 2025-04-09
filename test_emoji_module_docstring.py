import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_analyze_0(self):
        string = "Hello world 🌍"
        result = list(emoji.analyze(string))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "Hello world ")
        self.assertEqual(result[1].value, "🌍")

    def test_emoji_analyze_1(self):
        string = "I love coding 💻"
        result = list(emoji.analyze(string, non_emoji=True))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].value, "I ")
        self.assertEqual(result[1].value, "love ")
        self.assertEqual(result[2].value, "coding ")
        self.assertEqual(result[3].value, "💻")

    def test_emoji_analyze_2(self):
        string = "Let's eat 🍕🍔"
        result = list(emoji.analyze(string, non_emoji=True))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].value, "Let's ")
        self.assertEqual(result[1].value, "eat ")
        self.assertEqual(result[2].value, "🍕")
        self.assertEqual(result[3].value, "🍔")

    def test_emoji_analyze_3(self):
        string = "Family 👨‍👩‍👧‍👦"
        result = list(emoji.analyze(string, join_emoji=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "Family ")
        self.assertEqual(result[1].value, "👨‍👩‍👧‍👦")

    def test_emoji_analyze_4(self):
        string = "Happy New Year 🎉🎆"
        result = list(emoji.analyze(string, non_emoji=True, join_emoji=False))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].value, "Happy ")
        self.assertEqual(result[1].value, "New ")
        self.assertEqual(result[2].value, "Year ")
        self.assertEqual(result[3].value, "🎉🎆")

if __name__ == '__main__':
    unittest.main()

# End of Code
