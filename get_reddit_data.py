# user must install praw using pip install praw
import praw
# user must install emoji using pip install emoji
from emoji import UNICODE_EMOJI

"""
Create a Read-only Reddit Instance.

Initialize the Reddit class by passing in 3 keyword arguments.
The client ID, client secret, and user agent come from
the reddit application I created.
This is a global variable, so it is not inside a function.
"""
reddit = praw.Reddit(
    client_id="zhltW3UxNv6QSw",
    client_secret="KOTlq_YCgSS2xnB0v62NbtMFvf4",
    user_agent="OnionTitleScraper:v1 (by u/toOnionOrToNotOnion)"
)


def get_reddit_titles_top(subreddit_name):
    """
    Pulls as many titles from the top posts from a subreddit
    as possible, and puts each title as a string into a list

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    for submission in reddit.subreddit(subreddit_name).top(limit=None):
        title_list.append(submission.title)
    return(title_list)


def get_reddit_titles_new(subreddit_name):
    """
    Pulls as many titles from the new posts from a subreddit
    as possible, and puts each title as a string into a list

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    for submission in reddit.subreddit(subreddit_name).new(limit=None):
        title_list.append(submission.title)
    return(title_list)


def get_reddit_titles_hot(subreddit_name):
    """
    Pulls as many titles from the hot posts from a subreddit
    as possible, and puts each title as a string into a list

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    for submission in reddit.subreddit(subreddit_name).hot(limit=None):
        title_list.append(submission.title)
    return(title_list)


def get_reddit_titles_controversial(subreddit_name):
    """
    Pulls as many titles from the controversial posts from a subreddit
    as possible, and puts each title as a string into a list

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    for submission in \
            reddit.subreddit(subreddit_name).controversial(limit=None):
        title_list.append(submission.title)
    return(title_list)


def get_reddit_titles_rising(subreddit_name):
    """
    Pulls as many titles from the rising posts from a subreddit
    as possible, and puts each title as a string into a list

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    for submission in reddit.subreddit(subreddit_name).rising(limit=None):
        title_list.append(submission.title)
    return(title_list)


def get_reddit_titles_list(subreddit_name):
    """
    Pulls as many titles from a subreddit as possible,
    and puts each title as a string into a list.

    Pulls the post titles from as many top, new, hot,
    controversial, and rising posts from a subreddit as
    possible, and puts each title as a string into a list.
    It also removes duplicate titles, as a title that has been
    reposted more or in multiple categories should not have
    more weight when generating new titles.

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the collected titles as strings.
    """
    title_list = []
    # Adds all the titles from the categories into one list
    title_list += (get_reddit_titles_top(subreddit_name))
    title_list += (get_reddit_titles_new(subreddit_name))
    title_list += (get_reddit_titles_hot(subreddit_name))
    title_list += (get_reddit_titles_controversial(subreddit_name))
    title_list += (get_reddit_titles_rising(subreddit_name))
    # Removes duplicate titles
    title_list = list(dict.fromkeys(title_list))
    return(title_list)


def get_reddit_titles_word_list(subreddit_name):
    """
    Pulls as many titles from a subreddit as possible,
    and puts the words of each title as a string into a list.

    Pulls the post titles from as many top, new, hot,
    controversial, and rising posts from a subreddit as
    possible, and puts each title as a string into a list.
    It also removes duplicate titles, as a title that has been
    reposted more or in multiple categories should not have
    more weight when generating new titles.
    Lastly, it splits the title into individual words, and
    gives the first and last words of the title a special
    idenifying character (^ for the start, * for the end)

    Args:
        subreddit_name: A string representing the name of the
            subreddit to pull posts from. The name does not
            include the r/ section of the name.

    Returns:
        A list containing all of the words of the collected titles
        as strings.
    """
    word_list = []
    title_list = get_reddit_titles_list(subreddit_name)
    print(f"Successfully pulled {len(title_list)} {subreddit_name} titles.")
    # Take each title, split it into words and add start and end characters
    for title in title_list:
        # Split the title into words
        title = (title.split())
        # If the word is an emoji, remove it.
        for word in title:
            if word in UNICODE_EMOJI:
                title.remove(word)
        # Add the start character to the first word of the title
        title[0] = "^" + title[0]
        # Add the end character to the last word of the title
        title[-1] = title[-1] + "*"
        word_list += title
    return word_list
