# Giveaway NFT bot

Bot that automatically signs up to NFT giveaways on Reddit!

<p align="center">
<img width="1277" alt="Screen Shot 2021-09-22 at 17 52 12" src="https://user-images.githubusercontent.com/25267873/135364902-7b07959c-f439-476f-a583-f75ad6e5b493.png">
</p>

## Getting started

Run: `pip install -r requirements.txt`.

## How it works

Select your bot configurations in `config.ini`, including your Reddit API key from [here](https://www.reddit.com/prefs/apps).

```
[Credentials]
API_REDDIT_CLIENT_ID
API_REDDIT_CLIENT_SECRET
API_REDDIT_USERNAME
API_REDDIT_USER_AGENT
API_REDDIT_PASSWORD

[Bot]
OPENSEA_WALLET
MAX_GIVEAWAYS
MIN_SECS_SLEEP
MAX_SECS_SLEEP

[Reddit]
REDDIT_SUBS
REDDIT_COMMENTS
REDDIT_EMOJIS
```

Then you just need to run the python script with `python giveaway_nft_bot.py`.

## Pseudocode

1. Login to Reddit using the `API_REDDIT_*` keys provided.
2. Iterate through the posts in the `REDDIT_SUBS` list specified that contain the keyword GIVEAWAY.
3. Check that we have not commented+upvoted on a post from this author before, to avoid participating on same giveaway from 2 different subs.
4. Check that our bot has not commented on the post before.
5. Upvote post.
6. Comment on post by randomly picking a comment from `REDDIT_COMMENTS`, adding `OPENSEA_WALLET` and picking a random nice emoji from `REDDIT_EMOJIS`.
7. Print information about a post. E.g.
```
URL:  https://www.reddit.com/r/opensea/comments/pgqzh8/cryptocartooneaters_nft_giveaway_one_winner_will/
TITLE:  CryptoCartoonEaters NFT Giveaway! One winner will be randomly selected on September 9th. Follow details in comments to win.
OPENSEA:  https://opensea.io/collection/crypto-cartooneaters
```
8. Open the Opensea link to the collectible/collection. This is because on most giveaways, favouriting the collectibe/collection is necessary. E.g. https://opensea.io/collection/crypto-cartooneaters.
9. Wait for a random time between `MIN_SECS_SLEEP` and `MAX_SECS_SLEEP` until next post. This is to avoid Reddit detecting us as a bot.
10. Stop when we reach `MAX_GIVEAWAYS`

## Say thanks

Using this method, you are able to get sick NFTs that may be worth a fortune in the future.

I just got my hands on **Goku eating a Burger** from **CryptoCartoonEaters** NFT collection, and they are my favourite.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25267873/135364920-1defbdcb-0664-4715-96a3-ffcb36f26792.png" width="300"/>
</p>

Feel free to thank me by sending me some nice NFT artwork to my Opensea wallet: 0x5c747aa296f8621a572881fe6386b6739c1b80f8

## Disclaimer

Although this is an interesting bot application you should note **Reddit rules**:

"_Votes must be cast by humans. That is, API clients proxying a human’s action one-for-one are OK, but bots deciding how to vote on content or amplifying a human’s vote are not. See the reddit rules for more details on what constitutes vote cheating._"

## Future improvements

Some future possible improvements could be to be even more automated. For example, by connecting your twitter/insta account and either retweet or like a post based on what the OP requires to participate on the giveaway.

If you are interested in improving the bot, feel free to contribute. You may use the jupyter notebook for faster development.
