# Vinh Truong 88812807 truongvb

import io
import sys
import re
from collections import OrderedDict, defaultdict
import json
import psutil
import os
import bs4
import math

global total_docs	

####################### PART 1 ############################
STOP_WORDS = {"a", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", 
              "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"}

# bookkeeping = json.load(open('Information/webpages_raw/bookkeeping.json'))
# path = "Information/webpages_raw/"


def tokenize(file_name):
	word_dict = defaultdict(int)

	for tok in re.findall(r"[a-zA-Z0-9]+", file_name):
		if (tok not in STOP_WORDS):
			tok = tok.lower()
			word_dict[tok] += 1

	return word_dict

# def sorter(word_dict):
# 	for x,  y in sorted(word_dict.items(), key = lambda xy: (-xy[1], xy[0])):
# 		print str(x), "-", str(y)
def indexer(block, stream, docID):
	while psutil.virtual_memory()[4] > 10000000:
		try:
			tup = tuple(next(stream))
			# print(tup)
			block[tup[0]][docID] = tup[1]
		except StopIteration:
			return

# def compress_to_file():
# 	global block
# 	with open("IIndex.txt", "w+") as file:
# 		pass

def index_creation():
	global total_docs
	block = defaultdict(lambda: defaultdict(int))
	tokens = []

	for root, directories, files in os.walk(".", topdown=False):
		for i in sorted(files):
			if ("." in i):
				continue
			docID = "{}/{}".format(root.split("/")[-1], i)
			entire = os.path.join(root,i)
			print("Found %s"%(entire))
			with open (entire, "r", encoding="utf-8") as file_name:

				######### parsing #################

				soup = bs4.BeautifulSoup(file_name, "html.parser")
				for tag in soup(["script", "style"]):
					tag.extract()
				text = soup.get_text()
				indexer(block, iter(tokenize(text).items()), docID)

				######### parsing dun #############
				total_docs += 1

				print(psutil.virtual_memory()[4])
				print("###########################################")

	with open("IIndex2.txt", "w+") as file:
		file.write(json.dumps(block))
	with open("total_docs.txt", "w+") as file:
		file.write(total_docs)

def search_term(index, term):
	global total_docs
	try:
		result = defaultdict(int)
		postings = index[term]
		df = len(postings)
		for doc, tf in postings.items():
			result[doc] = ((1 + math.log(tf, 10)) * (math.log(total_docs/df, 10)))
		return result
	except Exception as e:
		print(e)
		return defaultdict(int)

def search_phrase(index, phrase):
	global total_docs
	words = phrase.split()
	query_tf = defaultdict(int)
	for word in words:
		query_tf[word] += 1

	scores = defaultdict(float)
	length = defaultdict(float)
	potentials = set()
	for word in words:
		w_term = ((1 + math.log(query_tf[word], 10)) * (math.log(total_docs/len(index[word]), 10)))
		x = search_term(index, word)
		for doc, weight in x.items():
			scores[doc] += weight * w_term
			length[doc] = math.sqrt(length[doc]**2 + weight**2)
			potentials.add(doc)

	for doc in potentials:
		scores[doc] /= length[doc]

	return sorted(potentials, key=lambda x: scores[x], reverse=True)[:10]

			




if __name__ == "__main__":
	global total_docs
	if input("Would you like to create the index? y/n\n").lower() == "y":
		index_creation()
	with open("IIndex.txt", "r") as file:
		index = json.load(file)
	with open("./WEBPAGES_RAW/bookkeeping.json", "r") as file:
		bookkeeping = json.loads(file.read())
	with open("total_docs.txt", "r") as file:
		total_docs = int(file.read())
	print("LOADED!!!?!??!?")
	query = input("Enter a search query, \"q\" to quit:\n").lower()
	while (query != "q"):
		for link in search_phrase(index, query):
			print(bookkeeping[link])
		query = input("Enter a search query, \"q\" to quit:\n").lower()
			






