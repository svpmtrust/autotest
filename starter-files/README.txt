INSTRUCTIONS TO INSTALL VIRTUAL BOX AND VAGRANT

1.Copy and paste all the contents from pen drive.

2.Steps for installing "VirtualBox-4.3.4-91027-win".

	-->Run the "VirtualBox-4.3.4-91027-win" setup file.
	-->Click Next and install.

3.Install "Git-1.8.4-preview-20130916"
	
	-->Run the "Git-1.8.4-preview-20130916".
	-->Click Next and select the option "Run Git and included Unix tools from the Windows Command Prompt".
	-->Click Next and check whether the option "Checkout Windows-style, commit Unix-style line endings" is selected or not.
	-->Click Next and install.

4.Open command prompt and type "git clone http:192.168.1.103:8080/git/'username'.git".In this command instead of 'username' in the command
  your alloted username should be typed.

5.Steps for installing "Vagrant_1.4.0".
	
	-->Run the "Vagrant_1.4.0" setup file. 
	-->Click Next and install.
	-->Restart your system.


6.Go to the folder in which vagrant has been installed and go into ".vagrant.d" folder then copy and paste "precise 32" from the pendrive

7.In command prompt go to the folder in which you have cloned the files and type "vagrant up".

8.Now type "vagrant ssh" in the same command prompt.

9.Type "cd /vagrant" in that command prompt. After typing this command you will get "vagrant@precise32:/vagrant$:"

10.Go to the folder in which you have cloned all the files and unzip the file according to the language 
   in which you write your program. After extracting rename the folder with the name "Echo".
   Ex: if you write a program in C language unzip Echo-c.zip and rename the extracted folder "Echo-c" to "Echo".

11.Now in command prompt type "ls" and find out if the folder has been extracted.
  Ex: if you extract the folder Echo-c.zip you will get the file Echo-c

12.Now go to the folder by typing "cd "folder name""

13.Now compile and run the program.

14.Now go to the folder which has been unzipped before and then right click on the folder and select the option
    "Git Bash" and you will be seeing a new command prompt where the below instuctions have to be followed.

15.In the command prompt type "cd 'folder name'".

16.Then type "git add 'program name'".

17.Then type "git commit -m "comments""

18.Then type "git push origin master"

19.You will receive a mail with your program status.

