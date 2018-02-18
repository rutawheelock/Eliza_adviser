#!/usr/bin/python

"""
# CS 5761 PA 1 - "Eliza the Academic Advisor"
# Author: Ruta Wheelock
# Date: 9/18/2017


# Description:
# This program simulates a student's conversation with an academic advisor.
# The user can ask questions to the advisor using chat dialog in command prompt.
#
# To run the program execute ./eliza_adviser.py in termianl window from the location where this file is saved.
# To stop dialog with Eliza, type 'exit'
#
# At first Eliza will ask your name and major, and will store that information for later use.
# After that Eliza will check if your input matches any of regular expressions encoded in this program
# and replies with one of corresponding messages. Reply messages are rotated so that if you ask the same question twice, you will get different answers.
# Matching  regular expressions are listed in order of importance.
# For example, if the user asks: "I don't know how to register for classes", Eliza will match "I don't know" part and reply "I'm concerned that you don't know".
# However, if the user asks: "I wanted to know how to register for classes", the input will match "how to <X>" part
# and return the response: "That's a good question. Do you have any ideas how to <X>". 
# "I don't know.." expression is higher in the list than "how to ...", therefore it is matched first. 
# In case the input does not match any regular expression from the list,
# Eliza will get questions from cachedQuestions list. Those questions can be asked only once and are removed from the list after using them.
#
# The goal of the program isn't to provide useful academic information
# but rather demonstrate the power of regular expressions.
"""

import re

#Check if the input is word 'exit' ignoring the case. Used for exiting the program.
exitRE = re.compile(r'^\bexit\b$', re.IGNORECASE)
#Check for different ways how to tell your name. Like "My name is Ruta", "I'm Ruta Wheelock" or just "Ruta"
#Stores the name in a named group 'name'. Used for finding the users's name from input.
getNameRE = re.compile(r'^(My name is |I am |I\'m )?(?P<name>\b\w+\b)', re.IGNORECASE)
#Check for a negation. Used for determining whether the user has a major or any courses of interest.
#Matches any responses that start with "I don't...", "I'm undecided..." etc.
noMajorRE = re.compile(r"^i( do not| don't| have't| have not|\'m undecided|\'m undeclared| am undecided| am undeclared).*", re.IGNORECASE)


"""
# A list of lists that contain regular expressions, that are checked against the input text.
# In each list the first entry is a regular expression to be matched and the following entries are replies.
# Replies are rotated before they get used.
# Regular expression checking happend in a linear fashion from top to bottom.
"""

matches = [
    #Checks for offensive language. Looks for keywords f**k, sh*t, bi**h, bullshit anywhere in the text. 
    [r'.*\b(fuck|shit|suck?|bullshit)\b.*', r'I told you, such language is not permitted.', r'Please mind your language.', ],
    #Checks for a word "ass" anywhere in the text.
    [r'.*\bass\b.*', r'We are not talking about donkeys now.'],
    #Looks for a question at the end of the input. Matches if the sentence ends with ".. ask <optional word> question?".
    # For example "Can I ask question?" and "Can I ask another question?" would match.
    [r'.*(ask you|ask) (\w+\s)?question\?$', r"You betcha!", r"Of course. What would you like to know?"],
    #Check for words "hate" and "angry" anywhere in the input.
    [r'.*\b(hate|angry)\b.*', r'Please control your emotions.', r'Please calm down!'],
    #Check for words "worried", "nervous", "stressed", "anxious" anywhere in the input and use this word in response.
    #The word is saved in a named group <E> and retrieved by calling the group \g<E>
    [r".*(?P<E>\b(worried|nervous|stressed|anxious)\b).*", r"Have you considered meditation?", r"When you are \g<E>, how do you relax?"],
    #Checks for 2 or more exclamation points at the end of the sentence.
    [r'.*!!!*$', r"No need to be shouting here.", r'You are getting very emotional.'],
    #Looks for sentences that start with a phrase "I don't know" or "I do not know"
    [r'^i (do not|don\'?t) know\b.*', r'I am not sure you are trying hard enough.',  r'I am concerned that you do not know.',],
    #Look for sentences starting "I'm not <X>" or "I am not <X>" and respond using the rest of the sentence in <X> 
    [r"^i('m not| am not) (?P<X>\w+.*)", r"What makes you say that you are not \g<X>?",  r"Why do you think you are not \g<X>?"],
    #Look for "I love..", "I enjoy..", "I admire..", "I like.." anywhere in the input and use this emotion in response.
    [r".*i (?P<X>\b(love|enjoy|admire|like)\b).*",r"Good to hear that.",  r"What else do you \g<X>?"],
    #Check anywhere in the text for a question "when is <X>?" and use <X> in response
    [r'.*when is (?P<X>\w+.*)\?', r'Remember, \g<X> will come and go but the most important is what will you do after that?',
     r'Time is relative. Why do you want to know when is \g<X>?', ],
    [r'.*when does (?P<X>\w+.*) \w+\?', r'How does \g<X> make you feel?', r'Does \g<X> make you nervous?',],
    #Look for sentences starting "You are not " or "You aren't "
    [r'.*^you (are not|aren\'t) .*', r'Looks like you do not appreciate my help.', r'It is not about me but your academic success.', ],
    #Check for questions that match "how many <X> I <Y>" anywhere in the text and reply using the input <X>, <Y> 
    [r'.*how many (?P<X>\w+) i (?P<Y>\w+.*)', r'How many \g<X> do you think you \g<Y>'],
    #Check for questions that match "how many <X1> <X2> I <Y>" anywhere in the text and reply using <X1>, <X2>, <Y>
    [r'.*how many (?P<X1>\w+) (?P<X2>\w+) i (?P<Y>\w+.*)', r'How many \g<X1> \g<X2> do you expect you \g<Y>'],
    #Check for questions "how can i <X>", "how should i <X>", "how do i <X>", "how to <X>" anywhere in the text
    #and use <X> in reply
    [r'.*how (can i|should i|do i|to) (?P<X>\w+.*)', r"Why do you want to know how to \g<X>?", r"That's a good question. Do you have any ideas how to \g<X>"],
    #Check for gibberish - input that contains letters and digits in one word
    [r'.*\w+\d+\w+\d+.*', r"I didn't quite understand. Can you say that another way?", r'I am not clear what you mean by that. Can you clarify?'],
]

"""
#Eliza uses questions from chachedQuestion list  when the user input does not match any regular expression in the matches list
#At the beginning of the dialog, appropriate question about the user's major is added to this list.
#Questions are removed from the list after using them.
"""
cachedQuestions = [
    "Is there anything else you would like to ask?",
    "Have you thought about what would you like to do after college?",
    "How do you like college life so far?",
]

"""
Helper function:
Takes in the user input "rawText" as an argument
and loops through regular expressions in the "matches" looking for a match. 
If the match is found, return correstponding list with regular expression and all replies, and call rotateReplies() function
If the match is not found, return false.
"""
def findMatch(rawText):
    for i, phrase in enumerate(matches):
        match = re.search(phrase[0], rawText,  re.IGNORECASE);
        if match:
            matchedPhrase = matches[i];
            rotateReplies(i);
            return matchedPhrase;
     
    return False


"""
Helper function:
Takes in the index of "matches" list where replies need to be rotated.
Pops the last item and inserts it into the position 1 using build-in list functions pop() and insert()
"""
def rotateReplies(index):
    lastItem = matches[index].pop()
    matches[index].insert(1, lastItem)

    
def main():
    print "This is Eliza The Academic Advisor, programmed by Ruta Wheelock.\n"

    """
    Intro block. Eliza asks for name an major.
    """
    
    print "->[eliza] Hi, I'm an academic advisor. What is your name?"
    someinput = raw_input("=> ");
    #Check different ways how to tell your name and save the name in a group 'name'
    getName = getNameRE.match(someinput);
    #Retrieve the named group 'name' from regular expression and save it
    name = getName.group('name');
    print "->[eliza] Nice to meet you, %s." % name;

    print "->[eliza] What is your major?";
    someinput = raw_input("=>[%s] " % name);
    #If response is a negation, assume the person does not have a major
    if noMajorRE.match(someinput):
        print "->[eliza] That is ok. What is your favourite course so far?"
        favouriteCourse = raw_input("=>[%s] " % name);
        print "->[eliza] Interesting."
        #check if the response is not a negation and append appropriate question to cachedQuestions list for later use
        if not noMajorRE.match(favouriteCourse):
            cachedQuestions.append("You said that you like %s. What makes it interesting?" % favouriteCourse);
        else:
            cachedQuestions.append("You mentioned that you don't have your favourite course. Why so?");
    #If response was not a negation, assume the user entered major.        
    else:
        major = someinput;
        print "->[eliza] %s is a great field." % major;
        cachedQuestions.append("You said that your major is %s. Why did you choose it?" % major);

    """
    Main block. Eliza prompts for input until user types 'exit'
    """
    print "->[eliza] How can I help you today?";
    while True:
        someinput = raw_input("=>[%s] " % name);
        #Check if the input was 'exit'
        doneTalking = exitRE.search(someinput);

        #Look for matching regular expressions by calling findMatch() method
        foundIt = findMatch(someinput);
        
        if foundIt != False:
            #Use regular expression substitution for replies
            Reply = re.sub(foundIt[0], foundIt[1], someinput.lower());
            print "->[eliza] %s" % Reply
            
        #if user enters 'exit', quit the program
        elif doneTalking:
            break
        
        #if no matches were found, get a question from cachedQuestions list
        elif len(cachedQuestions) != 0:
            Reply = cachedQuestions.pop()
            print "->[eliza] %s" % Reply
            
        #otherwise just keep asking
        else:
            print "->[eliza] Do you have any other questions?"
        

if __name__ == "__main__":
    main()
