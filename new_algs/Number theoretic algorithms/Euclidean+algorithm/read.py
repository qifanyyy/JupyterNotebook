#!/usr/bin/env python
import sys
import operator
from math import sqrt
from critics_dictionary import critics

firstName = ""
secondName = ""

#Checks if person has seen/rated movie
def checkMovie(name, myMovie):
    for movie, rating in critics[name].items():
        if(myMovie == movie):
            return True
    return False

#Returns list of movies person has NOT seen/rated
def getMovieList(name):
    movieList = []
    for critic, ratings in critics.items():
        for movie, rating in ratings.items():
            if((critic != name) and (checkMovie(name, movie) != True) and (movie not in movieList)):
                movieList.append(movie)
    return movieList

# Returns rating given to movie by person passed in
def getRating(name, myMovie):
    for movie, rating in critics[name].items():
        if(movie == myMovie):
            return rating


def getFirstName():
    global firstName
    if(len(sys.argv) == 3):
        firstName = sys.argv[1]
    else:
        firstName = raw_input("First Name: ")
        if(firstName not in critics):
            print "Name not in dictionary. Try again."
            getFirstName()

def getSecondName():
    global secondName
    if(len(sys.argv) == 3):
        secondName = sys.argv[2]
    else:
        secondName = raw_input("Second Name: ")
        if(secondName not in critics):
            print "Name not in dictionary. Try again."
            getSecondName()

def euclidean(n1, n2):
    scores = []
    for movie1, rating1 in critics[n1].items():
        #print movie, " - ", rating
        for movie2, rating2, in critics[n2].items():
            if (movie1 == movie2):
                #print rating1, "vs", rating2
                scores.append(pow((rating2 - rating1), 2))
    return sqrt(sum(scores))

def pearson(n1, n2):

    x = []
    y = []
    for movie1, rating1 in critics[n1].items():
            for movie2, rating2, in critics[n2].items():
                if(movie1 == movie2):
                    #print rating1, "vs", rating2
                    x.append(rating1)
                    y.append(rating2)
    Ex = sum(x)
    #print "Ex:", Ex
    Ey = sum(y)
    #print "Ey:", Ey
    
    xy = sum([a*b for a,b in zip(x,y)])
    #print "x*y:", xy

    xx = sum([i**2 for i in x])
    #print "x^2:", xx
    yy = sum([i**2 for i in y])
    #print "y^2:", yy

    numerator = (len(x)*xy-(Ex*Ey))
    #print "Num:", numerator

    denominator = sqrt((len(x)*xx-(Ex**2))*(len(x)*yy-(Ey**2)))
    #print "Den: ", denominator

    return round(numerator/denominator, 2)

def getRecommendation(name):
    recommendations = {}
    movieSum = 0
    simSum = 0

    for movie in getMovieList(name):
        #print movie
        for critic, ratings in critics.items():
            if(critic != name):
                pearResult = pearson(name, critic)
                if(getRating(critic,movie) != None):

                    #print critic, "- 0"
                    #print "Pearson Score:", pearResult
                    #print "Sim x Score: 0\n"
                #else:
                    simSum += pearResult
                    rating = getRating(critic, movie)
                    #print critic, "-", rating
                    #print "Pearson Score:", pearResult
                    movieSum += round(pearResult * rating, 2)
                    #print "Sim x Score:", round(pearResult * rating, 2), "\n"
        #print "Movie Sum: {}".format(movieSum)
        #print "Similarity Sum: {}".format(simSum)
        #print "Movie Sum / Similarity Sum: {}".format(round(movieSum/simSum, 2))
        recommendations.update({movie : round(movieSum/simSum, 2)})
        #recommendations[movie] = round(movieSum/simSum, 2)
        movieSum = 0
        simSum = 0
        #print "\n"

    return recommendations

def main():
    
    name = "Toby"
    
    recc = list(reversed(sorted(getRecommendation(name).items(), key=operator.itemgetter(1))))

    print "Recommendations for {}:".format(name)
    for idx, rec in enumerate(recc):
        print idx+1, "-", rec[0], "-",rec[1]

if __name__ == "__main__":
    main()