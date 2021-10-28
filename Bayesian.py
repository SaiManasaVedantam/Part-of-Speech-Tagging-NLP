import re
import sys

# Returns bigram probabilities for the tag bigrams
# key: bigram & value: probability
def findBigramProbs(tagCounts, bigramTagCounts):
    bigramProbs = dict()
    for bigram in bigramTagCounts:
        tag1, tag2 = re.split("\s+", bigram)
        bigramProbs[bigram] = bigramTagCounts[bigram] / tagCounts[tag1]
    return bigramProbs


# main function
if __name__ == '__main__':
    
    # Reads data from the text file specified in the command line
    dataset = sys.argv[1]
    testSentence = sys.argv[2]
    input_data = open(dataset).readlines()
    
    # Dictionary of the form: {Word : {{tag1 : count1}, {tag2 : count2} ...} }
    wordAndTagCounts = dict()
    
    # Dictionary of the form: {Tag1 : Count1, Tag2 : Count2 ...}
    tagCounts = dict()
    
    # Dictionary of the form: {Bigram1 : Count1, Bigram2 : Count 2 ...}
    bigramTagCounts = dict()
    
    
    # As input is read line by line, for each line, we perform preprocessing
    for line in input_data:
        line = line.strip()
        
        # Split by spaces to get unprocessed tokens
        words = re.split("\s+", line)
        
        # Counts that help us track <s> & </s> tags respectively
        startCount, endCount = 1, 1
        
        # Tracks <s> counts and stores it in tagCounts
        if "<s>" in tagCounts.keys():
            startCount += tagCounts.get("<s>")
        tagCounts["<s>"] = startCount
        
        # For bigram, intially we have <s>
        previous = "<s>"
        
        # Splits each word based on _ and identifies actual word & tag in it
        for w in words:
            if "_" in w:
                word, tag = w.split("_")
                wordTagCount = 1
                
                # Checks if the word already exists
                if word in wordAndTagCounts.keys():
                    values = wordAndTagCounts.get(word)
                    # If so, check if  corresponding tag exists for that word & update the count
                    if tag in values.keys():
                        wordTagCount += values.get(tag)
                        values[tag] = wordTagCount
                        wordAndTagCounts[word].update(values)
                   
                    # If not, add this new {tag : count} to the word
                    else:
                        wordAndTagCounts[word].update({tag : wordTagCount})
                        
                # If the word is not already present, add it to the dictionary with current {tag : count} for the word
                else:
                    wordAndTagCounts[word] = {tag : wordTagCount}
                
                # Checks if the tag already exists & updates/adds its count to the dictionary
                tagCount = 1
                if tag in tagCounts.keys():
                    tagCount += tagCounts.get(tag)
                tagCounts[tag] = tagCount
                
                # Creates bugram with previous & current tags
                bigram = previous + " " + tag
                bigramCount = 1
                
                # Checks if the bigram already exists & updates/adds its count to the dictionary
                if bigram in bigramTagCounts.keys():
                    bigramCount += bigramTagCounts.get(bigram)
                bigramTagCounts[bigram] = bigramCount
                
                # Updates previous tag to be useful for next bigram
                previous = tag
        
        # For bigram, at the end we have </s>
        bigram = previous + " " + "</s>"
        bigramCount = 1
        if bigram in bigramTagCounts.keys():
            bigramCount += bigramTagCounts.get(bigram)
        bigramTagCounts[bigram] = bigramCount
        

        # Tracks </s> counts and stores it in tagCounts
        if "</s>" in tagCounts.keys():
            endCount += tagCounts.get("</s>")
        tagCounts["</s>"] = endCount
      
        
    # Obtain bigram probabilities for the tag sequences
    bigramProbs = findBigramProbs(tagCounts, bigramTagCounts)

    # Computing bigram probability useing Naives Bayes for given test sentence using the above three cases
    # Preprocessing test sentence input
    testSentence = testSentence.strip()
    testTokens = re.split("\s+", testSentence)
    testWords = []
    testBigrams = []
    previous = "<s>"
    
    # Test input preprocessing
    for w in testTokens:
        if "_" in w:
            word, tag = w.split("_")
            testWords.append(word)
            testBigrams.append(previous + " " + tag)
            previous = tag
    testBigrams.append(previous + " " + "</s>")
       
    # Obtains test words maximum probable tag assignment for test words
    testResultTags = []
    maxProb = -1
    maxTag = ""
    
    for word in testWords:
        maxProb = -1
        maxTag = ""
        
        # Checks if the word already exists
        if word in wordAndTagCounts.keys():
            values = wordAndTagCounts.get(word)
        
            # Obtains tag counts
            previousTag = "<s>"
            for tag in tagCounts:
                countOfWordGivenTag = 0
                if values:
                    if tag in values.keys():
                        countOfWordGivenTag = values.get(tag)
                
                countOfTag = tagCounts.get(tag)
                countOfPreviousTag = tagCounts.get(previousTag)
                bigram = previousTag + " " + tag
                countOfBigram = 0
                
                # Checks if the bigram exists
                if bigram in bigramTagCounts:
                    countOfBigram = bigramTagCounts.get(bigram)
                
                probOfBigram = countOfBigram / countOfPreviousTag
                probOfWordGivenTag = countOfWordGivenTag / countOfTag
                
                # Computes probability
                product = probOfWordGivenTag * probOfBigram
                
                if product > maxProb :
                    maxProb = product
                    maxTag = tag
                previousTag = tag
        
        # If word is not in Corpus, we can't process it
        else:
            print("This word does not exist in the Corpus", word)
            print("So, we exit here")
            sys.exit()
            
        testResultTags.append(maxTag)
    
    # Displays final result
    print("\n----- POS TAGGING RESULT -----")
    result = ""
    for i in range(len(testWords)):
        result += testWords[i]+ "_"+ testResultTags[i] + " "
        
    print(result, "\n")
