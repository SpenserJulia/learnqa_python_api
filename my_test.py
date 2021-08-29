class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase:")
        print(f"{phrase}")

        assert len(phrase) <= 15, "Phrase longer then 15 simbols"