import logging
import random
import sys

import tweepy


log = logging.getLogger(__name__)


def test_words(prefix, subword, suffix, portmanteau):
    conditions = [
        prefix in suffix,
        suffix in prefix,
        portmanteau == prefix + "d",
        portmanteau == prefix + "e",
        portmanteau == prefix + "ing",
        portmanteau == prefix + "s",
        portmanteau == prefix + "ed",
        portmanteau == prefix + "ly",
        portmanteau == prefix + "es",
        portmanteau == prefix + "r",
        portmanteau == prefix + "er",
        portmanteau == prefix + "est",
        portmanteau == prefix + "iest",
        portmanteau == prefix + "ier",
        portmanteau == prefix + "able",
        suffix == subword + "ing",
        suffix == subword + "s",
        suffix == subword + "d",
        suffix == subword + "ed",
        suffix == subword + "ly",
    ]
    for condition in conditions:
        if condition:
            return False
    return True


def set_subwords(words, f):
    d = {}
    for word in words:
        subword = f(word)
        if subword in d:
            d[subword].append(word)
        else:
            d[subword] = [word]
    return d


def get_portmanteau(N, first_words, second_words):
    last_ns = set_subwords(first_words, lambda w: w[-N:])
    first_ns = set_subwords(second_words, lambda w: w[:N])

    n_trials = 2 * len(last_ns)
    for _ in range(n_trials):
        subword = random.choice(list(last_ns.keys()))
        if subword not in first_ns:
            continue
        prefix = random.choice(last_ns[subword])
        suffix = random.choice(first_ns[subword])
        portmanteau = prefix[:-N] + suffix
        if test_words(prefix, subword, suffix, portmanteau):
            return prefix, suffix, portmanteau
    return None, None, None


def main():
    twitter_consumer_key = sys.argv[1]
    twitter_consumer_secret = sys.argv[2]
    twitter_access_key = sys.argv[3]
    twitter_access_secret = sys.argv[4]
    twitter_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    twitter_auth.set_access_token(twitter_access_key, twitter_access_secret)
    twitter_client = tweepy.API(twitter_auth)

    with open("words.txt", "r") as f:
        words = [line.rstrip() for line in f]

    while True:
        N = random.randint(2, 4)
        prefix, suffix, portmanteau = get_portmanteau(N, words, words)
        if prefix is not None and suffix is not None:
            tweet = f"#{prefix} + #{suffix} = #{portmanteau}"
            try:
                twitter_client.update_status(tweet)
            except tweepy.TweepError:
                log.exception("tweepy failed on tweet: %s", tweet)
            break


if __name__ == "__main__":
    main()
