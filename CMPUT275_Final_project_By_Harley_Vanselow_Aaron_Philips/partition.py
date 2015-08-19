

def even_partition(inputlist):
    """
    This function utilizes dynamic programming to evenly distribute a list of integers into two sublists whose sums are
    are as close to equal as possible to the half of the sum of the elements in the original list. This is used in our
    game as a balancing feature to even the odds if one team has an unfair amount of units versus the other.
    The balancing is on a list of unit costs, and so doesn't neccesarily even the teams out in best way in terms of strategy
    just team cost. used http://people.cs.clemson.edu/~bcdean/dp_practice/ http://en.wikipedia.org/wiki/Partition_problem#The_k-partition_problem
    for doctests, sometimes there is more than 1 correct answer so these tests are not foolproof.
    As for runtime: O(n*m) where n is the number of elements in the list, and m is the number of sums (from adding elements in the sublist)
    that can be arranged from selecting elements into sublists. sums are keys in the inner dictionary and thus are not recounted in each inner dictionary.
    These two values are multiplied with each other due to the nested loops over keys i and j, with only constant operation within

    >>> even_partition([3,1,1,2,2,1])
    ([3, 1, 1], [2, 2, 1])
    >>> even_partition([-2,4,6])
    ([4], [-2, 6])

    """
    #sum of the elements in the given list
    bestsum=sum(inputlist)
    #will be used to store the one of the sets that holds a sum approximately (as close to) equal to half the bestsum 
    idealset=[]
    #used to compare if the ideal set's sum
    idealsplit=bestsum/2
    #initializes a nested dictiionary whose keys (at second/ deper level) are values, and the the list that these key point to the are elements 
    #from the input list that can sum up to the key value. The ditinary is nested to speed up the next iteration of the defining the dictionary
    P={}
    #intial values ie 0 is always made by the empty subset
    P[-1]={0:[]}
    for i in range(len(inputlist)):
        #gets first item from the list to start adding to subsets in inner dicts
        #initalies inner dicts with values 0,1...len(inputlist)-1
        Ai=inputlist[i]
        P[i]={}
        
        # computes inner dicts using previous inner dict stored in outer dict
        for j in P[i-1].keys():
            #reusing values
            P[i][j] = P[i-1][j]
            #getting next inner dict value by using previous inner dict then adding element to 
            #previous value and then adding to the element to the sublist the value points to
            P[i][j+Ai] = P[i-1][j] + [Ai]
            #making sure conditions are still met ie subset at most having a sum of the idealsplit value
            if abs((j+Ai)-idealsplit)<abs(bestsum-idealsplit):
                #if so redefine total sum, each time it gets larger by adding another element for input, while still keeping the conditions
                bestsum = j+Ai
                #idealset becomes the largest (by length) and closest whose sum is closest in value to the idealsplit, if not the next iteration would 
                #a subset whose sum is closer (still not larger than idealsplit) by adding another element while still upholding the conditions
                idealset= P[i][j+Ai]
    

    #properly returns both subsets
    for i in idealset:
        inputlist.remove(i)
    return idealset,inputlist




if __name__ == "__main__":
    import doctest
    doctest.testmod()