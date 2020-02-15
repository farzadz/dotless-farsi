alpha = u'ءأئؤآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
dotlessalpha = u'ءأئؤآاٮٮٮٮححححددرررسسصصططععڡٯکگلمںوهی'
mapping = dict(zip(alpha, dotlessalpha))

def translate(text):
    result = []
    for i, letter in enumerate(text):
        if letter in mapping:
            # handling yeh character (ی)
            if ord(letter) == 1740 and not (i == len(text)-1 or text[i+1] not in alpha):
                result.append(chr(1646))
            else:
                result.append(mapping[letter])
        else:
            result.append(letter)
    return ''.join(result)
