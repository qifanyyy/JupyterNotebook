
orb_price = [6.9,19.9,42.9,64.9,84.9,129.9,249.9]
orb_amount = [3,10,23,35,48,75,140]
print "Insert total money willing to spend"
money = input ()
amount = money
orb_bought = []
orb_total = 0
orb_buy = 0
flag = 1
repeat = 1
i = 0

while i<=6:
    k = i-1
    print "We will now analyze the orb deal of",orb_amount[i], "orbs"
    while repeat==1:
        #THIS DEALS WITH ORB TRANSACTIONS FOR A SINGLE ORB DEAL!
        repeat=0

        if flag==1:
            times_purchased = amount//orb_price[i]
            print "You purchased the",orb_amount[i],"orb deal a total of",times_purchased,"times"
            remaining = money - times_purchased * orb_price[i]
             
            print "Therefore, you bought..."
            orb_buy = orb_amount[i]*times_purchased
            print "...",orb_buy,"orbs"
            orb_total = orb_total + orb_buy
            print"You have now a total of",orb_total,"orbs."
            print "You have",remaining,"remaining"
            flag=0

            
        else:
            times_purchased = amount//orb_price[k]
            print "Since you have money left,",remaining,"to be precise..."
            print "You managed to purchase the deal of",orb_amount[k],"orbs a total of",times_purchased,"times"
            remaining = remaining - times_purchased*orb_price[k]
            print "You have",remaining,"remaining"
            
            print "Therefore, you bought..."
            orb_buy = orb_amount[k]*times_purchased
            print "...",orb_buy,"orbs"
            orb_total = orb_total + orb_buy
            print"You have now a total of",orb_total,"orbs."


        


        while k>=0 and i>0:
            if remaining>=orb_price[k]:
                repeat=1
                break
            k = k-1
        amount = remaining
    orb_bought.insert(i,orb_total)
    orb_total = 0
    orb_buy = 0
    flag = 1
    repeat = 1
    amount = money
    i = i+1
    if i<=6:
        print "Lets go to the next orb deal!"
    else:
        print "We've now calculated the total of orbs..."
        print "For every deal!"
    print "-------"
print "List with the orb deals:"
print orb_amount
print "List with total orbs purchased, in order of orb deals:"
print orb_bought
print "In which you buy the maximum amount possible with each deal."
print "You should buy therefore the..."
print orb_amount[orb_bought.index(max(orb_bought))],"deal"
