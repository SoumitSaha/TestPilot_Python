import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_analyze_0(self):
        string = "Hello 👋"
        result = list(emoji.analyze(string))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "Hello ")
        self.assertEqual(result[1].value, "👋")

    def test_emoji_analyze_1(self):
        string = "Good morning 🌞"
        result = list(emoji.analyze(string))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "Good morning ")
        self.assertEqual(result[1].value, "🌞")

    def test_emoji_analyze_2(self):
        string = "Python is fun! 😎"
        result = list(emoji.analyze(string, non_emoji=True))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "Python is fun! ")
        self.assertEqual(result[1].value, "😎")
        self.assertTrue(result[1].is_emoji)

    def test_emoji_analyze_3(self):
        string = "Emoji test 🔥💯"
        result = list(emoji.analyze(string, join_emoji=False))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "Emoji test ")
        self.assertEqual(result[1].value, "🔥")
        self.assertEqual(result[2].value, "💯")

    def test_emoji_analyze_4(self):
        string = "Let's code 🤖💻"
        result = list(emoji.analyze(string, non_emoji=True, join_emoji=False))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].value, "Let's code ")
        self.assertEqual(result[1].value, "🤖")
        self.assertEqual(result[2].value, "💻")
        self.assertTrue(result[1].is_emoji)
        self.assertTrue(result[2].is_emoji)

if __name__ == '__main__':
    unittest.main()

# End of Code
