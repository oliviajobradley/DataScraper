# Onion or Not?
## Reddit News Title Markov Generator

## Description
In this project, I used second-order Markov generation to produce news article titles. To gather the titles, I used Reddit's API to pull the titles of posts from news based subreddits. I pulled from r/TheOnion and r/nottheonion, but some other applicable subreddits are r/news, r/politics, and other subreddits with strict rules where the post titles can only be news titles.

The functions will lead you to markov generate titles and compare to see which titles are unique.

## Requirements

There are two packages that must be installed.
First is the praw package to access the reddit data. This can be installed using:
```
$ pip install praw
```
The second package is emoji, which can be installed using:
```
$ pip install emoji
```

## Usage
How to generate a list of titles and analyze how many titles are unique.
```python
import second_order_markov

"""
subreddit_name: A string representing the name of the
    subreddit to pull posts from. The name does not
    include the r/ section of the name.
num_sentences: A positive integer representing the number
    of titles to generate.
"""

second_order_markov.markov_generate_multiple_titles("name of subreddit", num_sentences)
# Return a list of generated titles.
second_order_markov.pie_chart_percentage_duplicates(subreddit_name, num_sentences)
# Return a pie chart that displays the percentage of generated titles
# that are unique (not the same as a source title) and that are
# duplicates (the same as a source title).
second_order_markov.unique_markov_titles(subreddit_name, num_sentences)
# Return a list of generated titles that are unique (not the same as a source title).
```
## Sources
Helpful resources for accessing the Reddit API:
- Creating an application for Reddit: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
- Quickstart Guide for using the Python Reddit API Wrapper (PRAW): https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

Helpful resource for implementing second-order Markov generation in python: https://medium.com/@jdwittenauermarkov-chains-from-scratch-33340ba6535b
