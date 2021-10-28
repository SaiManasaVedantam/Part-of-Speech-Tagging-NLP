# Part-of-Speech-Tagging-NLP
In Natural Language Processing, tagging or associating the appropriate part of speech (POS) tag to the word is extremely essential because POS tag helps us to understand the word sense in the **context** considered.

In general, the naive but the fundamental approach with which this process started is using **Bayesian Probabilistic method** where we consider the probability of a tag sequence for a word sequence can be obtained as: 

<img width="341" alt="Screen Shot 2021-10-27 at 10 42 34 PM" src="https://user-images.githubusercontent.com/28973352/139182814-daddb6f3-b48f-456f-84b4-e329071e1773.png">

On the other hand, one most commonly used and a better way of doing this is by using **Brill's Transformation Based Tagging.** In this, to find the probabilities, we consider the following steps:
1. Tagging the corpus with the most likely tag for each word i.e; Unigram model.
2. Choosing a transformation that replaces an existing tag with another such that the resulting tagged corpus has the lowest error rate out of all transformations.
3. Applying this transformation to the corpus i.e; we make the tagging better incrementally.
4. Iterating through this until some threshold is reached.
5. Returning as tagger the one that first tags using unigrams and then applies the learned transformations in that order.

In this project, I performed the Part-of-Speech tagging using the above two methods.

**To execute, use:**

python Brills.py Corpus.txt <"input_text">

Eg: python Brills.py Corpus.txt "Brainpower_TAG ,_TAG not_TAG physical_TAG plant_TAG ,_TAG"

python Bayesian.py Corpus.txt <"input_text">
	
Eg: python Bayesian.py Corpus.txt "Brainpower_TAG ,_TAG not_TAG physical_TAG plant_TAG"
