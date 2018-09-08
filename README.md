Hello everyone! This repo is a utilization of the links that are obtained through the web-crawler,
but the only information needed to construct the search engine is:
  1. URLs
  2. HTML of each URL
 
This search engine runs off a general formula called tf-idf, which gives a score to URLs based on the user's
search query. Tf-idf stands for term frequency inverted document frequency. In this case, each URL = document.

What this means is that for a given query, a score will be added to each URL for each word in the query.
A document that has many uses of the query term will have a higher score. The fewer amount of
documents that have the query term will give documents that DO have the term a higher score.

To make the calculation of tf-idf faster, we must construct and Inverted Index. This Inverted Index is implemented
as a hash table; each term is a key, and in the value we store another hash table. The nested hash table has keys
of each document, and the value is the term frequency score of the document.

  {term1: {doc1: 5, doc2: 7, ...}, term2: {doc1: 3, doc3: 4, ...}}
 
The outer dictionary is the Inverted Index, and each inner dictionary is called a Postings List. Having these two
components allows for quick computation of tf-idf scores.

After completing the calculation for raw, unedited tf-idf scores, I implemented different modifiers for each term found.
For instance, if the search term was found inside a header tag, then I'd give it more weight than a term
found in the body tag.

Since storing this Inverted Index in a raw form can take up huge amounts of space (originally, my index was ~100MB), I
compressed the terms by simply writing to a file with an underscore separation between each term.
The postings list for each term is compressed by storing the delta document ID, rather than storing each document ID.
This saves space especially for terms found across many documents. 

  For instance, if a list has two docIDs: 100000, 100001
  we would instead store the docIDs as  : 100000, 1
  
If we were storing this in a .txt file, then we saved 5 bytes by compressing one term.

After implementing a simple version of these two compressions, the total space of the inverted index is ~45MB! More than
half the space saved than just using json.dumps!

A future improvement is to use a database program (such as MySQL, MongoDB, etc.)
