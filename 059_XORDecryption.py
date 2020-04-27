"""
Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using p059_cipher.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.

ans: 129448
"""

from _data.p059 import get_data

def str_to_ascii(s):
	return [ord(c) for c in s]
	
def ascii_to_str(a):
	s = ""
	for c in a:
		s += chr(c)
	return s

def xor(code, key):
	d = []
	i = 0
	for c in code:
		d.append(c ^ key[i])
		i = (i + 1) % len(key)
	return d
	
def main():
	common_words = ["the"] # this one word is enough to decrypt the text
	ascii = [a for a in range(ord('a'), ord('z')+1)]
	data = get_data()

	min_word_len = min([len(s) for s in common_words])
	max_word_len = max([len(s) for s in common_words])
	common_words = [str_to_ascii(w) for w in common_words]
	data_len = len(data)

	max_match = -1
	max_key = None
	
	for a in ascii:
		for b in ascii:
			for c in ascii:
				data = get_data()
				data = xor(data, [a,b,c])
				
				match_count = 0
				start_index = 0
				while start_index < len(data):
				
					found = False
					for window in range(min_word_len, max_word_len + 1):
						if data[start_index:start_index + window] in common_words:
							start_index += window
							match_count += 1
							found = True
					if not found:
						start_index += 1
						
				if match_count > max_match:
					max_match = match_count
					max_key = [a,b,c]
					if match_count > 10: # arbitrary
						return max_key
	return max_key
	
max_key = main()

ans = xor(get_data(), max_key)
print(ascii_to_str(ans))
print("key: " + ascii_to_str(max_key))
print("sum: " + str(sum(ans)))