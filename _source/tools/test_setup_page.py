"""Regression checks for repeated finishing and exclusive setup chapters."""
import unittest
from setup_page import finish_setup_html

class SetupFinishingTest(unittest.TestCase):
    def fixture(self, declarations=''):
        return "<details class=\"chapter\" id=\"first\"></details><details class=\"chapter\" id=\"last\"></details>\nconst chapters=[...document.querySelectorAll('.chapter')];\n" + declarations + "const openFromHash=()=>{\nconst id=decodeURIComponent(location.hash.slice(1));\n};\naddEventListener('hashchange',openFromHash);\nif(location.hash)requestAnimationFrame(openFromHash);\n"

    def test_repairs_duplicate_declaration(self):
        result = finish_setup_html(self.fixture('const initialHash=location.hash;\n' * 2))
        self.assertEqual(result.count('const initialHash=location.hash;'), 1)

    def test_repeated_finishing_is_unchanged(self):
        once = finish_setup_html(self.fixture())
        self.assertEqual(finish_setup_html(finish_setup_html(once)), once)

    def test_native_exclusive_group(self):
        result = finish_setup_html(self.fixture())
        self.assertEqual(result.count('name="setup-chapters"'), 2)
        self.assertIn('id="first"', result)
        self.assertIn('id="last"', result)

    def test_initial_fragment_and_hash_changes(self):
        result = finish_setup_html(self.fixture())
        self.assertIn('if(initialHash)requestAnimationFrame(()=>openFromHash(initialHash));', result)
        self.assertIn("addEventListener('hashchange',()=>openFromHash());", result)

if __name__ == '__main__':
    unittest.main()
