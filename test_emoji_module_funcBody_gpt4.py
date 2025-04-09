import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_analyze_0(self):
        string = "I love Python 🐍"
        result = list(emoji.analyze(string))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "I love Python ")
        self.assertEqual(result[1].value, "🐍")

    def test_emoji_analyze_1(self):
        string = "Happy Birthday 🎉🎂"
        result = list(emoji.analyze(string, non_emoji=True))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].value, "Happy ")
        self.assertEqual(result[1].value, "Birthday ")
        self.assertEqual(result[2].value, "🎉")
        self.assertEqual(result[3].value, "🎂")

    def test_emoji_analyze_2(self):
        string = "No emoji here!"
        result = list(emoji.analyze(string, non_emoji=True))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "No ")
        self.assertEqual(result[1].value, "emoji ")
        self.assertEqual(result[2].value, "here!")

    def test_emoji_analyze_3(self):
        string = "Join emojis 👨‍👩‍👧‍👦"
        result = list(emoji.analyze(string, join_emoji=True))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "Join emojis ")
        self.assertEqual(result[1].value, "👨‍👩‍👧‍👦")

    def test_emoji_analyze_4(self):
        string = "Multiple emojis 👩‍🚀🌕🌍"
        result = list(emoji.analyze(string, non_emoji=True, join_emoji=True))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "Multiple emojis ")
        self.assertEqual(result[1].value, "👩‍🚀")
        self.assertEqual(result[2].value, "🌕🌍")

if __name__ == '__main__':
    unittest.main()

# End of Code
