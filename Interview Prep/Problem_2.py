def question2(a):

	a = a.lower()
	def is_palindrome(a):   #returns T/F
		return str(a) == str(a)[::-1]
	
	longest_palindrome = ""

	i = 0
	j = 1

	#new value can't be longest palindrome if len(string[i:j]) <= len(longest palindrome)
	while i < (len(a) - len(longest_palindrome)):
		#don't look beyond the possible indexes
		if j <= len(a):
			temp_string = a[i:j]
			#only worth checking if it is eligible to be the longest 
			if len(temp_string) > len(longest_palindrome):
				if is_palindrome(temp_string) == True:
					longest_palindrome = temp_string
			j += 1
		#move forward one place, start over
		else:
			i += 1
			j = i+1

	return longest_palindrome



print question2("racecar")
print question2("cumquat")
print question2("her name was anna the terrible")
print question2("anna drove a racecar")
print question2("sdfghjhgf")
print question2("abcdefg") 
print question2("Anna is taking the kayak to the river") 







	