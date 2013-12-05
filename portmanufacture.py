import random
import tweepy, time

def testWords(prefix,joint,suffix):
    portmanteau = prefix[:-N]+suffix
    conditions = [prefix in suffix,
                  suffix in prefix,
                  portmanteau == prefix+'d',
                  portmanteau == prefix+'e',
                  portmanteau == prefix+'ing',
                  portmanteau == prefix+'s',
                  portmanteau == prefix+'ed',
                  portmanteau == prefix+'ly',
                  portmanteau == prefix+'es',
                  portmanteau == prefix+'r',
                  suffix == joint+'ing',
                  suffix == joint+'s',
                  suffix == joint+'d',
                  suffix == joint+'ed',
                  suffix == joint+'ly']
    for condition in conditions:
       if condition:
          return False
    return True

def GetPortmanteau(N):
    f = open('words.txt','r')
    words = []
    firstNs,lastNs = {},{}
    for line in f:
        word = line.rstrip().decode('utf-8')
        words.append(word)
        try:
            firstNs[word[:N]].append(word)
        except:
            firstNs[word[:N]] = [word]
        try:
            lastNs[word[-N:]].append(word)
        except:
            lastNs[word[-N:]] = [word]

    found = False
    while not found:
        joint = random.choice(lastNs.keys())
        try:
            prefix = random.choice(lastNs[joint])
            suffix = random.choice(firstNs[joint])
            if testWords(prefix,joint,suffix):
                found = True
        except KeyError:
            continue

    return prefix, suffix, prefix[:-N]+suffix

f = open('auth.txt')
lines = [x.rstrip() for x in f.readlines()]
CONSUMER_KEY = lines[0] # To get this stuff, sign in at https://dev.twitter.com/ and Create a New Application
CONSUMER_SECRET = lines[1] # Make sure access level is Read And Write in the Settings tab
ACCESS_KEY = lines[2] # Create a new Access Token
ACCESS_SECRET = lines[3] # Shhhhhhhhh....
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

Going = True
N = 5
while Going:
    prefix,suffix,portmanteau = GetPortmanteau(N)
    print prefix, suffix, portmanteau
    api.update_status(prefix+' + '+suffix+' = '+portmanteau+' #portmanteau')
    time.sleep(3600) # Sleep for 1 hour (3600 seconds)
