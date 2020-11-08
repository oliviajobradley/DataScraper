import pytest

from second_order_markov import (
    build_word_dict,
    choose_first_word,
    generate_title,
    generate_text,
    markov_generate_multiple_titles,
    compare_generated_same_as_real,
    pie_chart_percentage_duplicates,
    unique_markov_titles,
)


# Define sets of test cases.

build_word_dict_cases = [
    # Check that if the source is 2 words long, return an empty dictionary
    (["word1", "word2"], {}),
    # Check that the start symbol does not mess with the dictionary
    # creation process
    (["^word1", "word2", "word3"], {("^word1", "word2"): ["word3"]}),
    # Check that the end symbol does not mess with the dictionary
    # creation process
    (["word1", "word2", "word3*"], {("word1", "word2"): ["word3*"]}),
    # Check that the dictionary can map two words to the same tuple
    (["w1", "w2", "w3", "w1", "w2", "w4"], {('w1', 'w2'): ['w3', 'w4'], (
        'w2', 'w3'): ['w1'], ('w3', 'w1'): ['w2']}),
]


choose_first_word_cases = [
    # Check that it returns the index of the word with the start character
    (["^word1", "word2", "word3"], 0),
    # Check that it returns the index of the word with the start character
    # when there is an end character
    (["word1", "word2*", "^word3"], 2),
    # Check that it returns the index of the word with the start character
    # when there is a start character in a different position in
    # in another word
    (["^word1", "word^2", "word3"], 0),
    # Check that it returns the index of the word with the start character
    # when there are multiple start characters in a row
    (["^^^word1", "word^", "word3"], 0),
]

generate_title_cases = [
    # Generate a title with a start and end.
    ({("^word1", "word2"): ["word3*"]}, ["^word1", "word2", "word3*"], "word1 word2 word3"),
    # Generate a short title with no dictionary.
    ({}, ["^word1", "word2*"], "word1 word2")
]

generate_text_cases = [
    # Generate multiple titles
    ({("^word1", "word2"): ["word3*"]}, ["^word1", "word2", "word3*"], 3, ["word1 word2 word3", "word1 word2 word3", "word1 word2 word3"]),
    # Generate multiple short titles with no dictionary.
    ({}, ["^word1", "word2*"], 4, ["word1 word2", "word1 word2", "word1 word2", "word1 word2"])
]

# Define standard testing functions to check functions' outputs given
# certain inputs defined above.


@pytest.mark.parametrize("source,dictionary", build_word_dict_cases)
def test_build_word_dict(source, dictionary):
    assert build_word_dict(source) == dictionary


@pytest.mark.parametrize("source,first_word", choose_first_word_cases)
def test_choose_first_word(source, first_word):
    assert choose_first_word(source) == first_word


@pytest.mark.parametrize("dictionary,source,title", generate_title_cases)
def test_generate_title(dictionary, source, title):
    assert generate_title(dictionary, source) == title


@pytest.mark.parametrize("dictionary,source,num,text", generate_text_cases)
def test_generate_text(dictionary, source, num, text):
    assert generate_text(dictionary, source, num) == text
