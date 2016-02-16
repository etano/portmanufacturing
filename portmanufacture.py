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
                  portmanteau == prefix+'er',
                  portmanteau == prefix+'est',
                  portmanteau == prefix+'iest',
                  portmanteau == prefix+'ier',
                  portmanteau == prefix+'able',
                  suffix == joint+'ing',
                  suffix == joint+'s',
                  suffix == joint+'d',
                  suffix == joint+'ed',
                  suffix == joint+'ly']
    for condition in conditions:
       if condition:
          return False
    return True

def GetPortmanteau(N, trends=None):
    f = open('words.txt','r')
    firstNs,lastNs = {},{}
    for line in f:
        word = line.rstrip().decode('utf-8')
        try:
            firstNs[word[:N]].append(word)
        except:
            firstNs[word[:N]] = [word]
        if trends == None:
            try:
                lastNs[word[-N:]].append(word)
            except:
                lastNs[word[-N:]] = [word]
    if trends != None:
        for trend in trends:
            try:
                lastNs[trend[-N:]].append(trend)
            except:
                lastNs[trend[-N:]] = [trend]

    found = False
    count = 0
    while not found:
        joint = random.choice(lastNs.keys())
        try:
            prefix = random.choice(lastNs[joint])
            suffix = random.choice(firstNs[joint])
            if testWords(prefix,joint,suffix):
                found = True
        except KeyError:
            continue
        count += 1
        if count > 2*len(lastNs.keys()):
            suffix = ''
            found = True

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
DoTrends = False
NoneFound = True
count = 0
while Going:
    N = random.randint(2,4)
    if count % 6 == 0:
        DoTrends = True
    if DoTrends:
        trends = [x['name'] for x in api.trends_place(23424977)[0]['trends'] if '#' not in x['name']] # US Trends
        prefix,suffix,portmanteau = GetPortmanteau(N, trends)
        if suffix == '':
            NoneFound = True
            DoTrends = True
        else:
            NoneFound = False
            DoTrends = False
    else:
        prefix,suffix,portmanteau = GetPortmanteau(N)
    print prefix,suffix,portmanteau
    if not NoneFound:
        try:
            f = open('ports.txt','a')
            f.write(prefix+' '+suffix+' '+portmanteau+'\n')
            f.close()
            api.update_status(prefix+' + '+suffix+' = '+portmanteau+' #portmanteau')
            count += 1
            time.sleep(7200) # Sleep for 2 hours (7200 seconds)
        except tweepy.TweepError as e:
            print 'ERROR: ', e
