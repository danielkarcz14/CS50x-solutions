import re


def main():
    text = input("Text: ")
    letters = len(extract_letters(text))
    words = len(extract_words(text)) + 1
    sentences = len(extract_sentences(text))
    # print grade
    print(colemanliau_index(letters, words, sentences))


def colemanliau_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    if index >= 16:
        return "Grade 16+"
    if index < 1:
        return "Before Grade 1"
    else:
        return f"Grade {round(index)}"


def extract_letters(text):
    return re.findall("[a-zA-Z]", text)


def extract_words(text):
    return re.findall(r"\s", text)


def extract_sentences(text):
    return re.findall(r"[.!?]", text)


if __name__ == "__main__":
    main()
