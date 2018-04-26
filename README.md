# RoboSub Vision Tools 2017/18
Someone needs to fill this out with instructions on how to install dependencies, run this script, add test cases, run test cases, add new components, why this repo matters, etc.  The multicamera_framework REDME.md can be used as a clear reference on how to fill this file out. General HTML codes work for normal things (<B>bold</B>, <I>italic</I>, etc).  Check https://www.stack.nl/~dimitri/doxygen/manual/markdown.html for more style codes and such.

<B>NOTE</B>:  You will need to install the doxygen and graphviz packages in order to run doxygen and generate the outputs.  You can do so with the following command on linux (windows users can blow me):

-  sudo apt-get install doxygen graphviz

Then cd into the doc directory and run the following:
  
-  doxygen config.dox

After the command runs, there will be an html/ directory.  Open html/index.html in your favorite web browser.

In general use case, the documentation does <I>not</I> get checked into the repository.  The idea being that code is changing so quickly, that if someone wants up to date documentation then they can download the repository themselves and run doxygen to generate the docs.

# Thanks. Your robot overlord, Bender.
