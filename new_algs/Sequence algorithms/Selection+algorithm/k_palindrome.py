"""
@author: David Lei
@since: 21/10/2017

http://www.geeksforgeeks.org/find-if-string-is-k-palindrome-or-not-set-2/

Longest palindromic subsequence of a string can easily be found using LCS. Following is the two step solution for finding longest palindromic subsequence that uses LCS.

Reverse the given sequence and store the reverse in another array say rev[0..n-1]
LCS of the given sequence and rev[] will be the longest palindromic sequence.
"""