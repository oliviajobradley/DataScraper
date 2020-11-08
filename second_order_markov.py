import random
from get_reddit_data import get_reddit_titles_word_list, get_reddit_titles_list
import matplotlib.pyplot as plt


def build_word_dict(source_text):
    """
    Build a dictionary mapping the previous two words to the
    next words that follow them in the source text.

    Map each pair of words to all words that follow it in the word list.
    Duplicates are included, and the list of words that follow a given
    pair are in the order in which they appear in the source text.
    The pairs are stored as a tuple, and the following words are
    stored as a string in a list.

    Args:
        source_text: A list containing all of the words of the
            collected titles as strings. Words that are at the
            beginning of the title start with the  character '^', and
            words at the end of the title end with the character '*'.

    Returns:
        A dictionary of mapped tuples and lists.
    """
    tuple_dictionary = {}
    number_of_words = len(source_text)
    # For every pair of words in the text, store them as a tuple.
    # Get the index and value of the first word
    for index, key1 in enumerate(source_text):
        # Get the index and value of the second word
        if number_of_words > index + 2:
            key2 = source_text[index + 1]
            following_word = source_text[index + 2]
            # Map each pair to the following word.
            # If the pair is new, add it
            if (key1, key2) not in tuple_dictionary:
                tuple_dictionary[(key1, key2)] = [following_word]
            # If the pair already has something mapped to it,
            # add the following word as another definition,
            else:
                tuple_dictionary[(key1, key2)].append(following_word)
    return tuple_dictionary


def choose_first_word(source_text):
    """
    Select the first word of the new title, making sure it begins with
    the start character '^'

    Args:
        source_text: A list containing all of the words of the
            collected titles as strings. Words that are at the
            beginning of the title start with the  character '^', and
            words at the end of the title end with the character '*'.

    Returns:
        An integer representing the location of the first word in
        the source text.
    """
    # Randomly choose the first word of the title
    first_word_int = random.randint(0, len(source_text) - 1)

    # If the first word does not have the start character, pick again
    first_word = source_text[first_word_int]
    while not (first_word[0] == '^'):
        first_word_int = random.randint(0, len(source_text) - 1)
        first_word = source_text[first_word_int]
    return (first_word_int)


def generate_title(tuple_dictionary, source_text):
    """
    Single sentence description, imperative.

    Longer description.

    Args:
        tuple_dictionary: A dictionary mapping the previous two words to a
            list of words that follow it in the source text, as described
            in the docstring for build_word_dict.
        source_text: A list containing all of the words of the
            collected titles as strings. Words that are at the
            beginning of the title start with the  character '^', and
            words at the end of the title end with the character '*'.

    Returns:
        A string representing the generated title.
    """
    # get first word of the title
    first_word = choose_first_word(source_text)
    # Find the key for that first word
    key = (source_text[first_word], source_text[first_word + 1])
    # Add the first two words to the title
    title = key[0] + ' ' + key[1]
    # Remove start character
    title = title[1:]

    # if the end of the second word has the end character,
    # remove it and end the sentence generation
    if title[-1] == '*':
        return title[:-1]

    # Begin adding the next word until the title becomes too long
    # (reddit has a 300 character title limit) or reaches and end character
    while len(title) < 300:
        current_word = random.choice(tuple_dictionary[key])
        # if not too long, add the next word to the title
        title += ' ' + current_word
        # if the word ends with the end character, remove the character and
        # return the title
        if current_word[-1] == '*':
            return(title[:-1])
        # if none of these, set the new key as the last two words
        # in order to find the next word
        key = (key[1], current_word)
    # when the length limit or end character has been reached return the title
    return title


def generate_text(tuple_dictionary, source_text, num_sentences):
    """
    Generate some number of random titles based on a dictionary of next
    words from a second order Markov model.

    Args:
        tuple_dictionary: A dictionary mapping the previous two words to a
            list of words that follow it in the source text, as described
            in the docstring for build_word_dict.
        source_text: A list containing all of the words of the
            collected titles as strings. Words that are at the
            beginning of the title start with the  character '^', and
            words at the end of the title end with the character '*'.
        num_sentences: A positive integer representing the number of titles
            to generate.

    Returns:
        A string representing the generated text.
    """
    multiple_generated_titles = []
    for sentence in range(num_sentences):
        multiple_generated_titles.append(generate_title(
            tuple_dictionary, source_text))
    return multiple_generated_titles


def markov_generate_multiple_titles(subreddit_name, num_sentences):
    """
    Generate some number of random titles based on a dictionary of next
    words from a second-order Markov model.

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.
        num_sentences: A positive integer representing the number
            of titles to generate.

    Returns:
        A string representing the generated text.
    """
    # Pull a list of titles from the subreddit
    source_text = get_reddit_titles_word_list(subreddit_name)
    # Create the dictionary of next words
    markov_dictionary = build_word_dict(source_text)
    # Markov generate a set of titles
    return(generate_text(markov_dictionary, source_text, num_sentences))


def compare_generated_same_as_real(subreddit_name, num_sentences):
    """
    Compare a set of generated tiles to the original titles to
    see if any of the generated titles are the exact same.

    Generate a set of titles, and compare them to the original
    titles from the subbreddit, if any are the same, add
    to the counter.

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.
        num_sentences: A positive integer representing the number
            of titles to generate.

    Returns:
        An integer representing the number of duplicate titles.
    """
    duplicate_counter = 0
    # Markov generate a number of titles in a list
    markov_titles = markov_generate_multiple_titles(
        subreddit_name, num_sentences)
    # Get the list of source titles
    source_text = get_reddit_titles_list(subreddit_name)
    # Compare the titles in either list to see if there are duplicates
    for generated_title in markov_titles:
        for real_title in source_text:
            # if there is a duplicate, add 1 to the counter and break
            # to the next generated title to compare
            if generated_title == real_title:
                duplicate_counter += 1
                break
    return duplicate_counter


def pie_chart_percentage_duplicates(subreddit_name, num_sentences):
    """
    Compare a set of generated tiles to the original titles to
    see if any of the generated titles are the exact same
    and visualize it in a pie chart.

    Generate a set of titles, and compare them to the original
    titles from the subbreddit, and count the number that are
    the same. Graph the amount that are duplicates and are
    unique on a labeled pie chart and display the chart.

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.
        num_sentences: A positive integer representing the number
            of titles to generate.
    """
    # Get the number of duplicate titles and unique titles
    duplicate_counter = compare_generated_same_as_real(
        subreddit_name, num_sentences)
    unique_counter = num_sentences - duplicate_counter

    # Pie chart, where the slices will be ordered and
    # plotted counter-clockwise:
    labels = 'Duplicate Titles', 'Unique Titles'
    sizes = [duplicate_counter, unique_counter]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is a circle.
    plt.title(f"Percent of generated r/{subreddit_name} titles "
              + f"that are the same as the source titles")
    plt.show()


def unique_markov_titles(subreddit_name, num_sentences):
    """
    Generate some number of random titles based on a dictionary of next
    words from a second order Markov model, while making sure none are
    the same as titles from the source.

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.
        num_sentences: A positive integer representing the number
            of titles to generate.

    Returns:
        A string representing the generated text.
    """
    duplicate_counter = 0
    # Markov generate a number of titles in a list
    markov_titles = markov_generate_multiple_titles(
        subreddit_name, num_sentences)
    # Get the list of source titles
    source_text = get_reddit_titles_list(subreddit_name)
    # Compare the titles in either list to see if there are duplicates
    for generated_title in markov_titles:
        for real_title in source_text:
            # if there is a duplicate, add 1 to the counter and break
            # to the next generated title to compare
            if generated_title == real_title:
                duplicate_counter += 1
                markov_titles.remove(generated_title)
                break
    # get the number of unique titles
    num_unique_titles = len(markov_titles)
    if num_unique_titles < num_sentences:
        markov_titles += unique_markov_titles(
            subreddit_name, num_sentences - num_unique_titles)
    return markov_titles
