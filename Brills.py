import re
import sys

# Stores words, associated tags & corresponsing counts respectively
corpusWordsList = []
correctTagsList = []
wordAndTagCounts = dict()


# Reads data from the text file specified in the command line
dataset = sys.argv[1]
testSentence = sys.argv[2]
input_data = open(dataset).readlines()
    
# As input is read line by line, for each line, we perform preprocessing
startAndEndCounts = 0
for line in input_data:
    line = line.strip()
        
    # Split by spaces to get unprocessed tokens
    words = re.split("\s+", line)
      
    # Appends start markers
    corpusWordsList.append("<s>")
    correctTagsList.append("<s>")
    
    # Splits each word based on _ and identifies actual word & tag in it
    for w in words:
        if "_" in w:
            word, tag = w.split("_")
            corpusWordsList.append(word)
            correctTagsList.append(tag)
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
     
    # Appends end markers
    corpusWordsList.append("</s>")
    correctTagsList.append("</s>")
    startAndEndCounts += 1
 
# Adds values for start & end markers
wordAndTagCounts["<s>"] = {"<s>" : startAndEndCounts}
wordAndTagCounts["</s>"] = {"</s>" : startAndEndCounts}               

# print(wordAndTagCounts)

# Find most likely tag for each word
mostLikelyWordTagPair = dict()

# Obtains most likely tag for each word in the Corpus
for word in wordAndTagCounts:
    values = wordAndTagCounts.get(word)
    maxCount = 0
    maxTag = ""
    for val in values:
        if values.get(val) > maxCount:
            maxCount = values.get(val)
            maxTag = val
    mostLikelyWordTagPair[word] = maxTag
    

# Now, set the most likely tag to each corresponding word in the corpus to know where errors occured which helps us to frame rules
currentTags = []
for word in corpusWordsList:
    currentTags.append(mostLikelyWordTagPair.get(word))
 
# Even before we apply any rule, we check initial error
error = 0
for i in range(len(currentTags)):
    if currentTags[i] != correctTagsList[i]:
        error += 1
# print(error)
    
# Get unique rules & tags
uniqueTags = []
for tag in correctTagsList:
    if tag not in uniqueTags:
        uniqueTags.append(tag)

uniqueTags.remove("<s>")
uniqueTags.append("<s>")
uniqueTags.remove("</s>")
uniqueTags.append("</s>")
uniqueRules = []

print("\n----------- Please wait until Rules are generated! ------------")

# Brill's Algorithm inplementation
first_iteration = True
best_rule = []
best_transform_score = 0

# Executes until sopme best rule is found
while first_iteration == True or len(best_rule) == 0:
    first_iteration = False
    prev_from_to_keys = []

    # For each tag
    for from_tag in uniqueTags:
        # To each tag
        # Initializations
        best_instance_score = 0
        #print("From: " + from_tag)
        best_Z  = ""
        for to_tag in uniqueTags:
            good_transforms = dict()
            bad_transforms = dict()
            max_score = 0
            score = 0
            
            #print("To:" + to_tag)
            # For each word in the corpus
            for word in range(1, len(correctTagsList)):
                correct_tag = correctTagsList[word]
                current_tag = currentTags[word]
                previous_tag = currentTags[word-1]
                key = previous_tag + " " + from_tag + " " + to_tag
                prev_from_to_keys.append(key)
                
                # Checks for case 1
                if correct_tag == to_tag and current_tag == from_tag:
                    if key in good_transforms.keys():
                        good_transforms[key] = 1 + good_transforms.get(key)
                    else:
                        good_transforms[key] = 1
                        
                # Checks for case 2    
                elif correct_tag == from_tag and current_tag == from_tag:
                    if key in bad_transforms.keys():
                        bad_transforms[key] = 1 + bad_transforms.get(key)
                    else:
                        bad_transforms[key] = 1


            # For all from-to-prev keys existing in the keyset
            for key in good_transforms.keys():
                score = good_transforms.get(key) - bad_transforms.get(key, 0)
                if score > max_score:
                    best_Z = key
                    max_score = score
                # print("Score: ", score, " Max-Score: ", max_score, " best_Z: ", key)
            
            
            # If it's better than the best_instance_score, update best_rule
            if max_score > best_instance_score:
                previousTag, fromTag, toTag =  re.split("\s+", best_Z)
                best_rule = [fromTag, toTag, previousTag]
                best_instance_score = max_score
                uniqueRules.append(best_rule)
                
            
            # Compares the instance & transform scores
            if best_instance_score > best_transform_score:
                best_transform_score = best_instance_score
            
            #print("Instance Score: ", best_instance_score, " Transform Score: ", best_transform_score, " best_Z: ", key)
            
            # Updates current tag after applying the best rule obtained on the corpus     
            for iteration in range(1, len(correctTagsList)):
                previousTag = correctTagsList[iteration-1]
                if currentTags[iteration] == best_rule[0] and previousTag == best_rule[2]:
                    currentTags[iteration] = best_rule[1]
                
   
print("Rules generated :)")
#for i in range(len(uniqueRules)):
    #print("--FROM--\t", uniqueRules[i][0], "\t---TO---\t", uniqueRules[i][1], "\t---PREVIOUS---\t", uniqueRules[i][2])

first = True
option = 0
while first == True or option == 1:
# Predicts POS tags for a test sentence based on rules
# As input is read line by line, for each line, we perform preprocessing
    testWords = []
    testCorrectTags = []
    
    # Test sentence preprocessing
    testSentence = testSentence.strip()
    
    # Split by spaces to get unprocessed tokens
    words = re.split("\s+", testSentence)   
    
    testWords.append("<s>")
    testCorrectTags.append("<s>")
       
    # Splits each word based on _ and identifies actual word & tag in it
    for w in words:
        if "_" in w:
            word, tag = w.split("_")
            if word not in corpusWordsList:
                print("The word " + word + " does not exist in the corpus")
                print("Exiting the Process")
                sys.exit()
            testWords.append(word)
            testCorrectTags.append(tag)
            
    testWords.append("</s>")
    testCorrectTags.append("</s>")
          
    # Most likely tags are assigned
    testCurrentTags = []
    for word in testWords:
        testCurrentTags.append(mostLikelyWordTagPair.get(word))
        
        
    # Apply rules on test input to obtain final tags
    for rule in uniqueRules:
        #print(rule)
        for pos in range(1, len(testWords)):
            previous_tag = testCorrectTags[pos-1]
            if testCurrentTags[pos] == rule[0] and previous_tag == rule[2]:
                testCurrentTags[pos] = rule[1]
                
                
    print("\n----- POS TAGGING RESULT -----")
    result = ""
    for i in range(1, len(testCurrentTags)-1):
        result += testWords[i] + "_" + testCurrentTags[i] + " "
    print(result)
    
    print("\n Do you want to continue?")
    option = int(input("1. Yes \t 2. No\n"))
    
    if option == 1:
        testSentence = input("Enter a test sentence: \n")
       
    elif option == 2:
        print("---- Exiting ----")
        break
    
    else:
        print("Invalid Choice")
        break
