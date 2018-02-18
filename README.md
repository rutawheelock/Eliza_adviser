# Eliza the Academic Advisor
Developed as an assignment for University of Minnesota Duluth course Intro to Natural Language Processing.  
Author: Ruta Wheelock  
Date: 9/18/2017  

## Description
This program simulates a student's conversation with an academic advisor.  
The user can ask questions to the advisor using chat dialog in command prompt.  

To run the program execute
```
./1PA.py
```
in termianl window from the location where this file is saved.  
To stop dialog with Eliza, type '**exit**'

At first Eliza will ask your name and major, and will store that information for later use.  
After that Eliza will check if your input matches any of regular expressions encoded in this program
and replies with one of corresponding messages. Reply messages are rotated so that if you ask the same question twice, you will get different answers.
Matching  regular expressions are listed in order of importance.  
For example, if the user asks: "I don't know how to register for classes", Eliza will match "I don't know" part and reply "I'm concerned that you don't know".
However, if the user asks: "I wanted to know how to register for classes", the input will match "how to <X>" part
and return the response: "That's a good question. Do you have any ideas how to <X>".   
"I don't know.." expression is higher in the list than "how to ...", therefore it is matched first.   
In case the input does not match any regular expression from the list,
Eliza will get questions from cachedQuestions list. Those questions can be asked only once and are removed from the list after using them.

The goal of the program isn't to provide useful academic information
but rather demonstrate the power of regular expressions.
