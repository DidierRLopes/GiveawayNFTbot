from psaw import PushshiftAPI
import praw
import random
import time
import configparser
import re
import webbrowser
import warnings

warnings.filterwarnings("ignore")

# Parse Config
cfg = configparser.RawConfigParser()
cfg.read("config.ini")

API_REDDIT_CLIENT_ID = eval(cfg["Credentials"]["API_REDDIT_CLIENT_ID"])
API_REDDIT_CLIENT_SECRET = eval(cfg["Credentials"]["API_REDDIT_CLIENT_SECRET"])
API_REDDIT_USERNAME = eval(cfg["Credentials"]["API_REDDIT_USERNAME"])
API_REDDIT_USER_AGENT = eval(cfg["Credentials"]["API_REDDIT_USER_AGENT"])
API_REDDIT_PASSWORD = eval(cfg["Credentials"]["API_REDDIT_PASSWORD"])

OPENSEA_WALLET = eval(cfg["Bot"]["OPENSEA_WALLET"])
MAX_GIVEAWAYS = eval(cfg["Bot"]["MAX_GIVEAWAYS"])
MIN_SECS_SLEEP = eval(cfg["Bot"]["MIN_SECS_SLEEP"])
MAX_SECS_SLEEP = eval(cfg["Bot"]["MAX_SECS_SLEEP"])

REDDIT_SUBS = eval(cfg["Reddit"]["REDDIT_SUBS"])
REDDIT_COMMENTS = eval(cfg["Reddit"]["REDDIT_COMMENTS"])
REDDIT_EMOJIS = eval(cfg["Reddit"]["REDDIT_EMOJIS"])

praw_api = praw.Reddit(
    client_id=API_REDDIT_CLIENT_ID,
    client_secret=API_REDDIT_CLIENT_SECRET,
    username=API_REDDIT_USERNAME,
    user_agent=API_REDDIT_USER_AGENT,
    password=API_REDDIT_PASSWORD,
)

l_post_author = []
psaw_api = PushshiftAPI()
submissions = psaw_api.search_submissions(
    subreddit=REDDIT_SUBS,
    q="GIVEAWAY|Giveaway|giveaway",
    filter=["id"],
)

n_giveaways_found = 1
while True:
    try:
        submission = next(submissions, None)

        # Check if search_submissions didn't get anymore posts
        if not submission:
            break

        # Get more information about post using PRAW api
        submission = praw_api.submission(id=submission.id)

        # Ensure that the post hasn't been removed  by moderator in the meanwhile,
        # that there is a description and it's not just an image, and that we aren't
        # re-considering same author's watchlist
        if (
            not submission.removed_by_category
            and submission.selftext
            and submission.author.name not in l_post_author
        ):
            text_from_op = submission.selftext

            have_seen_post_before = False
            for comment in submission.comments:
                # The bot has already commented here, so skip this post
                if comment.author.name == API_REDDIT_USERNAME:
                    have_seen_post_before = True
                # Comment from author it may contain the opensea url we are interested
                elif comment.author.name == submission.author.name:
                    text_from_op += comment.body

            # If we have see this post before, just skip it
            if have_seen_post_before:
                continue

            # If there's no reference to opensea, the giveaway may be in another chain
            # If the subreddit doesnt contain opensea name, then we are confident that the
            # the collection/item is in another chain. Thus, we skip this post
            if (
                "opensea" not in text_from_op.lower()
                and "opensea" not in submission.subreddit.display_name.lower()
            ):
                continue

            print("URL: ", submission.url)
            print("TITLE: ", submission.title)

            # Upvote post
            submission.upvote()

            # Comment on post
            comment = REDDIT_COMMENTS[random.randint(0, len(REDDIT_COMMENTS) - 1)]
            emoji = REDDIT_EMOJIS[random.randint(0, len(REDDIT_EMOJIS) - 1)]
            submission.reply(f"{comment} {OPENSEA_WALLET} {emoji}")

            # Extract opensea url
            try:
                opensea_url = re.search(
                    "(?P<url>https?://opensea.io[^\s]+)", text_from_op
                ).group("url")
                if opensea_url:
                    if "]" in opensea_url:
                        opensea_url = opensea_url.split("]")[0]
                    if ")" in opensea_url:
                        opensea_url = opensea_url.split(")")[0]
                    print("OPENSEA: ", opensea_url)
                    webbrowser.open(opensea_url)
            except:
                print("No Opensea URL")

            # Wait a random amount of time to avoid getting recognized as a bot
            secs_to_wait = random.randint(MIN_SECS_SLEEP, MAX_SECS_SLEEP)
            time.sleep(secs_to_wait)

            # Increment count of valid NFT giveaways posts found
            n_giveaways_found += 1

            # This avoids to comment on posts from same author across multiple subs
            l_post_author.append(submission.author.name)
            print("")

        # Check if number of wanted posts found has been reached
        if n_giveaways_found > MAX_GIVEAWAYS:
            break

    except:
        print("Error occurred!")

print("The end.")