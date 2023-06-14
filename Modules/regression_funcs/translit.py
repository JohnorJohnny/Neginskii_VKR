from assets.settings import ALPH


def translit(string):

    translit_string = ""

    for letter in string:

        translit_string += (
            ALPH.get(letter.lower(), letter.lower()).upper()
            if letter.isupper()
            else ALPH.get(letter, letter)
        )

    return translit_string
