from random import randint

from .database import get_db
from .models import Post

# Write your custom classes and functions here

# Estimating post reading time
def reading_time(content):
    """
    https://infusion.media/content-marketing/how-to-calculate-reading-time/
    """
    words = content.split()
    words = len(words)
    read_time = words / 200
    spliced_read_time = str(read_time).split(".")

    # If time has decimal places
    if spliced_read_time[1]:

        extra_time = ((int(spliced_read_time[1]) / 1000) * 0.60) * 100

        # If decimal places numbers smaller than 30 seconds return read_time without change and decimal places
        if extra_time < 30:
            final_time = int(spliced_read_time[0])
            return final_time

        # If decimal places numbers bigger than 30 seconds we add a minute to reading time
        final_time = int(spliced_read_time[0]) + 1
        return final_time

    # If read_time is round without decimal places
    final_time = read_time
    return final_time


# Random Post for using in index page
def random_post():
    db = get_db()

    # Count all posts in database
    posts_count = Post.objects().count()

    if posts_count:
        # Return a random post from all posts in database
        r_t = Post.objects()[[randint(0, posts_count - 1)][0]]
        return r_t

    # If posts == 0
    return 0
