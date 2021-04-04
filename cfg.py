import random
import itertools

DATA_PATH = "cfg.gr"

#---------------------------------------
class CYK:

	def rules(self, path):
		file = open(path, "r")
		flag = 0 
		rules = {}
		word_dict = {}
		for line in file:
			words = line.split()
			if(line != '\n' and words[0] != "ROOT" and words[0] != "#" and flag == 0):
				strin = ""
				for w in range(1, len(words)):
					strin += words[w] + " "
				if(words[0] not in rules):
					rules[words[0]] = [strin.strip()]
				else:
					rules[words[0]].append(strin.strip())
			if(line != '\n' and words[1] == "Vocabulary." ):
				flag = 1
			elif(line != '\n' and flag==1 ):
				word_dict[words[1]] = words[0]
			
		return rules, word_dict

	def select_rand_word_from_tag(self, word_dict, tag):
		words = []
		for k, v in word_dict.items():
			if (v==tag):
				words.append(k)
		return random.choice(words)


	def randsentence(self, word_dict, out_file_path, num_of_sent, sent_len):
		sentences = []
		out_file = open(out_file_path, "w")

		for i in range(num_of_sent):
			sent = ""
			for m in range(sent_len):
				w = random.choice(list(word_dict.keys()))
				sent += w + " "
			sentences.append(sent.split())
			out_file.write(sent + '\n')

		return sentences

	def CYKParser(self, rules, word_dict, sent):
		correct_or_not = 0
		sent_len = len(sent)
		curr_triang_len = len(sent)

		triangular_table = [] 

		#initiate triangular table with zeros according to sentence length
		for i in range(sent_len):
			tri = []
			for t in range(curr_triang_len):
				tri.append([])

			triangular_table.append(tri)
			curr_triang_len -= 1
		

		#first fill the base of triangular table
		for w in range(sent_len):
			curr_word = sent[w]
			tag = word_dict[curr_word]
			triangular_table[0][w].append(tag)
			for key, val in rules.items():
				if(tag in val):
					triangular_table[0][w].append(key)




		idx = 1
		for i in range(len(triangular_table[idx-1])):
			if(i+1 != len(triangular_table[idx-1]) ):
				#find all possible combinations for all below tags
				#print(triangular_table[idx-1][i], "*****", triangular_table[idx-1][i+1])
				for a, b in itertools.product(triangular_table[idx-1][i] , triangular_table[idx-1][i+1]) : 
					phrase = a+" "+ b
					#if current permutasyon of below two items in table is in rules
					#update current field of the table with this phrase
					for key, val in rules.items():
						if(phrase in val):
							triangular_table[idx][i].append(key)


		if("S" in triangular_table[sent_len-1]):
			correct_or_not = 1

		return correct_or_not


cyk_obj = CYK()

rules, word_dict = cyk_obj.rules(DATA_PATH)
#print(rules)  #{'S': ['NP VP'], 'VP': ['Verb NP'], 'NP': ['Det Noun', 'Pronoun', 'NP PP'], 'PP': ['Prep NP'], 'Noun': ['Adj Noun']}
sentences = cyk_obj.randsentence(word_dict, "output.txt", num_of_sent=10, sent_len=5)

for sent in sentences:
	result = cyk_obj.CYKParser(rules, word_dict ,sent)
	for s in sent:
		print(s ,end=" ")
	print(" -> ", end = "")

	res = "Not Correct"
	if (result == 1): 
		res="Correct"
	print(res)

