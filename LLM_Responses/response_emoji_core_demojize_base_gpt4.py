import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_demojize_0(self):
        result = emoji.demojize("😀")
        self.assertEqual(result, ":grinning_face:")

    def test_emoji_core_demojize_1(self):
        result = emoji.demojize("I love 🍕", delimiters=("", ""))
        self.assertEqual(result, "I love pizza")

    def test_emoji_core_demojize_2(self):
        result = emoji.demojize("🏃‍♀️", language='es')
        self.assertEqual(result, ":mujer_corriendo:")

    def test_emoji_core_demojize_3(self):
        result = emoji.demojize("🏃‍♀️", language='en', version=5.0)
        self.assertEqual(result, ":woman_running:")

    def test_emoji_core_demojize_4(self):
        custom_handle_version = lambda emoji, aliases: aliases.get(emoji, emoji)
        result = emoji.demojize("🏃‍♀️", handle_version=custom_handle_version)
        self.assertEqual(result, ":woman_running:")

if __name__ == '__main__':
    unittest.main()


#End of Code