def question1(s, t):
	#creates a dict of {character:character_frequency} pairs for all characters in a given string
	def create_dict(string):
		string_dict = {}
		for character in string:
			if character in string_dict:
				string_dict[character] += 1
			else:
				string_dict[character] = 1
		return string_dict

	#case where one does not exist
	if s == None or t == None:
		return False

	#case where strings are the same
	if s == t:
		return True

	#impossible for t to have an anagram substring of s if t is longer than s 
	if len(s) < len(t): 
		return False

	s = s.lower()
	t = t.lower()
	#create dicionaries from the strings
	t_dict = create_dict(t)
	s_dict = create_dict(s)
	#no anagram of t is a substring of s if s has less occurences of a character than t
	for character in t_dict: 
		if character not in s_dict:
			return False
		if s_dict[character] < t_dict[character]:
			return False 
	#an anagram substring exists if s has >= the number of occurences of each of t's characters as t 
	return True



print question1(None, 'a') #False
print question1('a', None) #False
print question1(None, None) #False
print question1('', '') #True
print question1('', 'a') #False
print question1('a', '') #True
print question1('abcd', 'abcde') #False
print question1("Udacty", "AD") #True
print question1("I am Sam", "Sam") #True
print question1("abc@#$", "@#$") #True
print question1("abc", "def") #False