from spellchecker import SpellChecker

def spelling_check(word):
    spell = SpellChecker(language = None, case_sensitive = True)
    spell.word_frequency.load_dictionary('ka-words.json')

    correct_word = spell.correction(word)
    return correct_word

def text_converter_checker(sentence):

    result = ""

    model_dictionary = {
            55 : " ",
            0 : "!",
            1 : ",",
            2 : "-",
            3 : ".",
            4 : "0",
            5 : "1",
            6 : "2",
            7 : "3",
            8 : "4",
            9 : "5",
            10 : "6",
            11 : "7",
            12 : "8",
            13 : "9",
            14 : "?",
            15 : "ა",
            16 : "ბ",
            17 : "გ",
            18 : "დ",
            19 : "ე",
            20 : "ვ",
            21 : "ზ",
            22 : "თ",
            23 : "ი",
            24 : "კ",
            25 : "ლ",
            26 : "მ",
            27 : "ნ",
            28 : "ო",
            29 : "პ",
            30 : "ჟ",
            31 : "რ",
            32 : "ს",
            33 : "ტ",
            34 : "უ",
            35 : "ფ",
            36 : "ქ",
            37 : "ღ",
            38 : "ყ",
            39 : "შ",
            40 : "ჩ",
            41 : "ც",
            42 : "ძ",
            43 : "წ",
            44 : "ჭ",
            45 : "ხ",
            46 : "ჯ",
            47 : "ჰ"
    }

    for letter in sentence:
        result = result + str(model_dictionary[int(letter)])

    final = ""

    for word in result.split():

        correct_word = spelling_check(word)

        if correct_word is None:
            final = final + word + " "
        else:
            final = final + correct_word + " "

            if word[-1] == ".":
                final = final[:-1] + "."

            if word[-1] == ",":
                final = final[:-1] + ", "

    return result, final

