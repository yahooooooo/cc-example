Insight Data Engineering - Coding Challenge
===========================================================

WordCount
-----------------------------------------------------------

The first problem in the coding challenge is Word Count, which takes in a text file or set of text files from a directory and outputs the number of occurrences for each word.  For example, Word Count on a file containing the following passage:

> So call a big meeting,  
Get everyone out out,  
Make every Who holler,  
Make every Who shout shout.  

would return:

	a			1
	big			1  
	call		1  
	every		2  
	everyone	1  
	get			1  
	holler		1  
	make		2  
	meeting		1  
	out			2  
	shout		2  
	so			1  
	who			2  

Word Count is implemented in a Python program named `my_word_count.py` that counts all the words from the text files contained in a directory named `wc_input` and outputs the counts (in alphabetical order) to a file named `wc_result.txt`, which is placed in a directory named `wc_output`. The program achieves scalability by performing parallel file processing on multicore machines, before merging the word count dictionaries obtained from different files.

Running Median
-----------------------------------------------------------

The second problem in the coding challenge is the Running Median - which keeps track of the median for a stream of numbers, updating the median for each new number.  Specifically, we need to implement a running median for the number of words per line of text.  For example, the first line of the passage

> So call a big meeting,  
Get everyone out out,  
Make every Who holler,  
Make every Who shout shout.  

has 5 words so the running median for the first line is simply 5.  Since the second line has 4 words, the running median for the first two lines is the median of {4, 5} = 4.5 (since the median of an even set of numbers is defined as the mean of the middle two elements after sorting).  After three lines, the running median would be the median of {4, 4, 5} = 4, and after all four lines the running median is the median of {4, 4, 5, 5} = 4.5.  Thus, the correct output for the running median program for the above passage is:

	5.0  
	4.5  
	4.0  
	4.5  

Running Median is implemented in a Python program named `my_running_median.py` that calculates the median number of words per line, for each line of the text files in the `wc_input` directory.  Multiple files in that directory are processed in parallel by the running median program in alphabetical order using the `concurrent.futures` multiprocessing API available in Python 3. The resulting running median for each line is written to a text file named `med_result.txt` in the `wc_output` directory. The program achieves scalability by performing parallel file processing on multicore machines to extract the word count by line, before performing the running median algorithm.

Requirements
-----------------------------------------------------------

The `run.sh` script needs Python3 to run correctly. The dependency is because of the use of the concurrent multiprocessing API.
