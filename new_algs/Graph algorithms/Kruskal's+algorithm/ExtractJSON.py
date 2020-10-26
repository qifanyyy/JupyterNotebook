#!/usr/bin/python
## This class is used for Bonus Task 6.1
## @author Shaanan Cohney 2013

import facebook
import json
import random


##REPLACE WITH YOUR APP ID AND APPSECRET
FACEBOOK_APP_ID = "350671815038483"
FACEBOOK_APP_SECRET = "658638184f0f6dbcc0c998ec694a9ff"

##REPLACE WITH UP TO DATE TOKEN
oauth_access_token = "AAAEZB7yT31hMBAJZAsSXzpN8ZAGBfb2QDcfWBKZCjz7uxUHqIgkZB8PKg4HtQ54zhQktSe0agfMptZCExwr7B9MqxU6mQw2tozgLyhMAUDlJgD37axLL4F"

#Previous Token used AAAEZB7yT31hMBAKHL4EwrRAdYlMed4UScM5YH1UxhkTpCELS79hMxhg1KkZBq1WWtjUnWICus2exlGWkPfAyWJFQGkfrxCqjamWDZB6ESRIym1emoDR


graph = facebook.GraphAPI(oauth_access_token)

SET_SIZE = 300
OFFSET = 0
nodes = 0

full = {}

f = open("output.log",'w')

ids = {}

try:
        profile = graph.get_object("me")
        friends = graph.get_connections("me","friends")
        i = 0
        
        ## Get all friends and friends of friends, scrambling names
        
        full[profile['id']] = {}
        full[profile['id']]['name'] = profile['name']
        full[profile['id']]['friends'] = []

        for friend in friends["data"]: 

                i+=1
                print(i)

                if i < OFFSET:
                        continue

                if (nodes > SET_SIZE) and ((friend['id'] in ids) == False):
                        continue

                full[profile['id']]['friends'].append(friend)
                

                if (friend['id'] in ids) == False:
                        ##Scramble Names - modify to just add name
                        ids[friend['id']] = ''.join(friend['name'])
                        nodes +=1

                friend['name'] = ids[friend['id']]
                full[friend['id']] = {}
                full[friend['id']]['name'] = friend['name']
                full[friend['id']]['friends'] = []

                ## Do same for mutual friends
                friends_friends = graph.get_connections(str(friend["id"]),"mutualfriends")
                for friends_friend in friends_friends["data"]:

                        if (nodes > SET_SIZE) and ((friends_friend['id'] in ids) == False):
                                continue

                        if (friends_friend['id'] in ids) == False:
                                nodes +=1
                                #Scramble Names - modify to just add name
                                ids[friends_friend['id']] = ''.join(friends_friend['name'])
                        


                        friends_friend['name'] = ids[friends_friend['id']]
                        full[friend['id']]['friends'].append(friends_friend)
                        

                ## Add root node to everyone's friends (we're getting 'mutual friends)
                full[friend['id']]['friends'].append({'name' : profile['name'], 'id' : profile['id']})
                

        f.write(json.dumps(full))

except facebook.GraphAPIError as e:
    print('Something went wrong:', e.type, e.message)

f.close()
