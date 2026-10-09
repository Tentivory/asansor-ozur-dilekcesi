import unittest
import asansor

class TestAsansor(unittest.TestCase):
    def test_bos_ozur_red(self):
        ok, _ = asansor.karar(4, "")
        self.assertFalse(ok)

    def test_hafif_ozur_red(self):
        ok, metin = asansor.karar(2, "ozur")
        self.assertFalse(ok)
        self.assertIn("REDDEDILDI", metin)

    def test_agir_ozur_kabul(self):
        ok, metin = asansor.karar(
            7,
            "Gec kaldigim icin ozur dilerim, rica ederim, saygilarimi sunarim, muhurum yanima.",
        )
        self.assertTrue(ok)
        self.assertIn("ONAYLANDI", metin)

    def test_yasak_kat(self):
        ok, _ = asansor.karar(13, "ozur dilerim rica ederim saygilar muhur")
        self.assertFalse(ok)

if __name__ == "__main__":
    unittest.main()
