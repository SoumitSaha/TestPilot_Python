import emoji
import unittest

class TestemojiModule(unittest.TestCase):
    def test_emoji_core_emoji_list_0_base(self):
        result = emoji.emoji_list('')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_1_base(self):
        result = emoji.emoji_list('Hello world!')
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2_base(self):
        result = emoji.emoji_list('Hello world! 😃')
        self.assertEqual(result, [{'match_start': 13, 'match_end': 14, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_3_base(self):
        result = emoji.emoji_list('😃😃😃')
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😃'}, {'match_start': 1, 'match_end': 2, 'emoji': '😃'}, {'match_start': 2, 'match_end': 3, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_4_base(self):
        result = emoji.emoji_list('Hello 😃 world! 😃😃')
        self.assertEqual(result, [{'match_start': 6, 'match_end': 7, 'emoji': '😃'}, {'match_start': 15, 'match_end': 16, 'emoji': '😃'}, {'match_start': 16, 'match_end': 17, 'emoji': '😃'}])

    def test_emoji_core_emoji_list_0_func_body(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_1_func_body(self):
        result = emoji.emoji_list("Hello World! 🌍")
        expected = [{'match_start': 13, 'match_end': 14, 'emoji': '🌍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_2_func_body(self):
        result = emoji.emoji_list("No emoji here.")
        expected = []
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_3_func_body(self):
        result = emoji.emoji_list("Multiple emojis 👍👍")
        expected = [{'match_start': 16, 'match_end': 17, 'emoji': '👍'}, {'match_start': 17, 'match_end': 18, 'emoji': '👍'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_4_func_body(self):
        result = emoji.emoji_list("Emoji at start 🎉 of the string.")
        expected = [{'match_start': 15, 'match_end': 16, 'emoji': '🎉'}]
        self.assertEqual(result, expected)

    def test_emoji_core_emoji_list_0_docstring(self):
        result = emoji.emoji_list("Hi, I am fine. 😁")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_1_docstring(self):
        result = emoji.emoji_list("No emojis here")
        self.assertEqual(result, [])

    def test_emoji_core_emoji_list_2_docstring(self):
        result = emoji.emoji_list("Multiple emojis 😁👍")
        self.assertEqual(result, [{'match_start': 16, 'match_end': 17, 'emoji': '😁'}, {'match_start': 17, 'match_end': 18, 'emoji': '👍'}])

    def test_emoji_core_emoji_list_3_docstring(self):
        result = emoji.emoji_list("😁 at the start")
        self.assertEqual(result, [{'match_start': 0, 'match_end': 1, 'emoji': '😁'}])

    def test_emoji_core_emoji_list_4_docstring(self):
        result = emoji.emoji_list("end with emoji 👍")
        self.assertEqual(result, [{'match_start': 15, 'match_end': 16, 'emoji': '👍'}])

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

#End of Code