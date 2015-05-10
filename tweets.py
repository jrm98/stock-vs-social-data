

def tweet_freq(users, num_docs, keywords):
	score_matrix = [0 for x in range(num_docs)]

	for user in users:
		txt = open('data/tweets/'+user+'.txt').read().lower()
		punc = '.,:;"\'-!?$@'
		for p in punc:
		    txt = txt.replace(p,'')
		tweets = txt.split('\n')

		doc_size = len(tweets) / num_docs
		docs = [tweets[x*doc_size:(x*doc_size + doc_size)] for x in range(num_docs)]

		# split the words:
		for x in range(len(docs)):
			for i in range(len(docs[x])):
				docs[x][i] = docs[x][i].split()

		for i in range(num_docs):
			doc = docs[i]

			# add to score matrix for each occurance of keywords
			for t in doc:
				for w in t:
					if w in keywords:
						score_matrix[i] += 1

	return score_matrix