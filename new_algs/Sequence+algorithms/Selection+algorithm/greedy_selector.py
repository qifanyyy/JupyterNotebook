a=[]
class greedy_algo():
    def greedy_selector(self, s, f,):
        
        n=len(s)
        A=[s[0]]
        k=1
        for m in range(2,n):
            if(s[m]>=f[k]):
                A.append(s[m])
                k=m
        return A



    def recursive_activity_selector(self, s, f, k, n,):
        m = k + 1
        while m < n and s[m] < f[k] and k >= 0:
            m = m + 1
        if m < n:
            a.append(s[m])
            self.recursive_activity_selector(s, f, m, n)
        else:
            return []
        return a

        

if __name__=="__main__":
    ob=greedy_algo()
    s = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]
    f = [5,4,9, 12, 9, 9, 16, 11, 15, 14, 10]
    greedy= ob.greedy_selector(s,f)

    print("Output Greedy Activity Selector: ")
    print(greedy)
    greedy2 =ob.recursive_activity_selector(s,f,-1,len(s))
    print("Output Recursive Activity Selector: ")
    print(greedy2)


