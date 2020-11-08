import pytest
# user must install praw using pip install praw
import praw

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

# Define standard testing functions

#@pytest.mark.parametrize()
@pytest.mark.timeout(1)
def test_connected_to_reddit():
    assert reddit.read_only == True
