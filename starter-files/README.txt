
RULES OF ENGAGEMENT
-------------------
1. We expect students to be honest and all the programs
   must be their own.  
2. Use of Internet, reference texts, cheat sheets (a.k.a. slips)
   is ALLOWED. 
3. Phone-a-Friend, Ask some one else to write the programs is
   NOT ALLOWED.  The person you are calling, or helping you
   can appear for the test instead :-) and we can hire him. 
4. You have about 6 hours to write the code.  If you are not done 
    with at least one easy problem in 3 hours, you should really asses your
    position. 
5. To proceed to the interview round you should score at least 15 points. 
6. Be ready to explain how your program works.  If you didn't
   write it, we will know very easily, and you will be asked to explain. 

INSTRUCTIONS
------------

1. Go to the folder in which you have cloned your question paper.  
2. A simple implementation for Echo is given to you already.  Go to the Echo directory and unzip
   the file for your favorite language. 
   
   Ex: If you write a program in C language unzip Echo-c.zip into the Echo   
   directory.
   
3. Now compile and run the program as per instructions below in command prompt.
  --> For compiling a program type "sh compile.sh".
  --> For running a program type "sh run.sh 'hi welcome to'"
  
   IMPORTANT: Each directory must have a compile.sh and run.sh so that
   your program is complied and executed properly.  Use the samples from
   Echo program to guide you. 
   
4. Commit the changes and push them for testing. 
	1. Type "git add run.sh compile.sh Echo.[c/java/py]" to let git know what files to merge.
	2. Type "git commit -m "comments""
	3. Type "git push origin" to send the code for testing. 

5.You can check your result in a few minutes with the status of your 
    program after automated test is complete in the UI.

6. Each program is allocated a maximum execution time.  If the program didn't finish 
   in the given time, it will be terminated, and the submission is considered a failure. 
   
7. Read each question carefully and make sure your output matches exactly what is requested. 
   Additional debugging output will invalidate your program as the validation
   code can't differentiate debug outputs from normal outputs. Remember your
   program is validated by dumb computers, they go super literal.  
   
8. You should not read from stdin.  I.e. getch(), scanf(), System.in.read(), etc are now allowed. 
   All the input comes either from a file whose name is given as argument, or as arguments itself.
   
9. THERE ARE NO WRONG QUESTIONS.  ONLY WRONG ANSWERS. 

LIST OF PROGRAMS
================
-------             ------   ----------
Program             Score    Difficulty
-------             ------   ----------
1.Echo  .  .  .  .  .  0     None (Curtesy Solution Provided Already)
2.Hyphenize   .  .  .  8     Easy
3.Banner      .  .  . 10     Easy


=========
GOOD LUCK
=========
