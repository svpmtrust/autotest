INSTRUCTIONS FOR USING VAGRANT AND GIT TO RUN THE PROGRAMS .

1.In command prompt go to the contest folder and in contest folder you will find a folder your user name
  and type "vagrant up".

2.Now type "vagrant ssh" in the same command prompt.

3.Type "cd /vagrant" in that command prompt. After typing this command you will get "vagrant@precise32:/vagrant$:"

4.Go to the folder in which you have cloned all the files and unzip the file according to the language 
   in which you write your program. 
   Ex:If you write a program in C language unzip Echo-c.zip.
   
5.After extracting rename the folder with the name "Echo".
   Ex: If you extract Echo-c then rename the extracted folder "Echo-c" to "Echo".  

6.Now in command prompt go to the folder by typing "cd "folder name""
  Ex: cd users/contest/username/Echo
  
7.Now compile and run the program as per instructions below in command prompt.

  --> For compiling a program type "sh compile.sh".
  --> For running a program type "sh run.sh 'hi welcome to'"

8.After compiling and running the program type "git add 'program name'".

9.Then type "git commit -m "comments""

10.Then type "git push origin master"

11.Now it will ask you a user name and password. For user name and password
   give your alloted user name. 

12.You will receive a mail with your program status.


LIST OF PROGRAMS IN THE CONTEST
===============================

-------             ------   --------------
Program             Score    Subject Matter   
-------             ------   --------------
1.Echo  .  .  .  .  .  1     Environment Setup
2.Palindrome  .  .  .  3     Basic Programming Skills
3.Expansion   .  .  .  5     Basic Programming Skills
4.Histogram   .  .  .  8     Data Structures
5.Sudoku   .  .  .  . 10     Data Structures and Algorithm Design
6.Maze .   .  .  .  . 15     Basic Artificial Intelligence using Recursion
7.Anagrams .  .  .  . 15     Data Structures and Advanced Programming Skills
8.Expression  .  .  . 20     Compiler Design
9.Pattern  .  .  .  . 25     Advanced Programming Skills
10.Puzzle3 .  .  .  . 30     Artificial Intelligence (Brute Force)                   
11.Puzzle4 .  .  .   100     Artificial Intelligence, requires use of Heuristics
                   ------
GRAND TOTAL          232
                   ------

=========
GOOD LUCK
=========