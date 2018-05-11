# RoboSub IMU Tools 2017/18
<B>Overview</B>
This framework connects any inertial measurement unit (IMU) to computer. This framework can operate on raspberry pi, 
ubuntu 16.04 and on windows with a few exceptions. The goal of this framework is to be modular, that is be able to 
take data from any IMU regardless of the connection and be user-friendly at the same time. This was done by extending 
a parent class functions and global variables to child classes. The child classes for each specific IMU then made 
the connection between the IMU and computer relaying the data to the framework in the exact same way. This allows 
for a user to get data from any IMU and have it output the same way for each them. 

<B>Data flow</B>
This framework is unique in the fact that the instance for the is past down from each test file to the tools and one 
more down to the memory bank where it gets instantiated. This is down so that each, if multiple IMU’s are called, 
have their own memory bank associated to them. This was done to reduce computer memory when this program is ran. 

<B>Adding new components</B>
All IMU’s that have been added thus far extend the global variables and functions from the parent class imu.py. 
This style should be implemented into all added IMU’s.

<B>NOTE</B>:  You will need to install the doxygen and graphviz packages in order to run doxygen and generate the outputs.  You can do so with the following command on linux (windows users can blow me):

-  sudo apt-get install doxygen graphviz

Then cd into the doc directory and run the following:
  
-  doxygen config.dox

After the command runs, there will be an html/ directory.  Open html/index.html in your favorite web browser.

In general use case, the documentation does <I>not</I> get checked into the repository.  The idea being that code is changing so quickly, that if someone wants up to date documentation then they can download the repository themselves and run doxygen to generate the docs.

# Thanks. Your robot overlord, Bender.
