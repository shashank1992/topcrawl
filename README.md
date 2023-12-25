# Python based web crawler to identify the key words for a given website

## Usage
Install the dependencies. 
from the repo run
python3 app.py --url=url --n=n --m=m

### args :
  url: The url to be parsed (enter the string)
  n: The number of key words or topics we wish to obtain. defaults to 10
  m: The multiplier factor for the double worded topics , defaults to 2. 

## Algorithm 

The problem of topic modelling, has been studied in great depth and there are numerous resources.
The most popular nlp libraries employ either NMF(non negative matrix factorization) or the LDA (Latent Dirchlent Allocation) to obtain the relevant topics.
The project uses a simple to understand and intuitive frequency based approach to identify the best topics.
Often times, complex libraries could have a learning curve and even a steeper one if customisations are intended, which often defeats the purpose of automation.
This project uses, a frequency based algorithm, that is not only intuitive but is easy to tweak.

## Can break down the algorithm into 3 steps
1. Identify the most popular (n) tokens, that become our topics in the text corpus.
2. Genenerate all possible two word combinations of the n tokens, and obtain their respective frequencies from the text corpus.
3. Combine the two sets of tokens ( which is like our bigger vocabulary) to obtain the new most popular (n) tokens.

This is inspired by the byte pair tokenisation employed by the famous BERT model. [Hugging Face implementation of BERT](https://huggingface.co/learn/nlp-course/chapter6/5?fw=pt)


