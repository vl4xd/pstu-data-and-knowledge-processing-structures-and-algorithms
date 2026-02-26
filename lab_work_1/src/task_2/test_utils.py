import unittest
from utils import MyInputAssistant


class TestMyInputAssistant(unittest.TestCase):

    def test_preprocessing_empty_text(self):
        mia = MyInputAssistant()
        self.assertEqual(mia._preprocessing(''), [])
        self.assertEqual(mia._preprocessing(' '), [])
        self.assertEqual(mia._preprocessing('\n'), [])
        self.assertEqual(mia._preprocessing('\t'), [])

    def test_preprocessing_only_letters_spaces_lowercase(self):
        mia = MyInputAssistant()
        self.assertEqual(
            mia._preprocessing('we study programming languages'),
            ['we', 'study', 'programming', 'languages']
        )

    def test_preprocessing_only_letters_spaces_uppercase(self):
        mia = MyInputAssistant()
        self.assertEqual(
            mia._preprocessing('WE STUDY PROGRAMMING LANGUAGES'),
            ['we', 'study', 'programming', 'languages']
        )

    def test_preprocessing_mixed_symbols_en(self):
            mia = MyInputAssistant()
            self.assertEqual(
                mia._preprocessing('We study programming languages C++, C#, Go.\nWe are programmers!'),
                ['we', 'study', 'programming', 'languages',
                 'c', 'c', 'go', 'we', 'are', 'programmers']
            )

    def test_preprocessing_mixed_symbols_ru(self):
        mia = MyInputAssistant()
        self.assertEqual(
            mia._preprocessing('Я создаю свой язык программирования - РуПитон2026++.'),
            ['я', 'создаю', 'свой', 'язык', 'программирования', 'рупитон']
        )

    def test_preprocessing_with_homoglyphs(self):
         mia = MyInputAssistant()
         # заглавными буквами выделены латинские буквы
         self.assertEqual(
              mia._preprocessing('я любила Eго. Oн CказAл, что не любит меня'),
              ['я', 'любила', 'eго', 'oн', 'cказaл', 'что', 'не', 'любит', 'меня']
         )

    def test_preprocessing_ignores_punctuation_and_brackets(self):
        mia = MyInputAssistant()
        self.assertEqual(
             mia._preprocessing('[Привет], "мир"! (Это) тест? - да.'),
             ["привет", "мир", "это", "тест", "да"]
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
