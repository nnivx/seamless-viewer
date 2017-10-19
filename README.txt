Requirements:

	python 3.x
	pygame

How to run seamless viewer:

python3 seamless-viewer.py regex [w h gap margin dir]

	regex - filename regex filter (check regex for more info)
	w - window width, default 1000
	h - window height, default 600
	gap - page gap, default 0
	margin - side margin in percentage, default 10

Features:

	S - stich the images and save it to 'save.png'
	nothing else, yes. not even zoom, lol

all arguments after the regex are strictly positional
example:

	# looks for ch1-p<number>.png filename in same directory
	python3 seamless-viewer.py "ch1-p\d.png"

	# open only specific range of pages
	python3 seamless-viewer.py "ch1-p[2-7].png"
	
	# open files from other directory
	python3 seamless-viewer.py "ch1-p\d.png" 1000 600 0 10 "path"

** for linux machines, you can run it as an executable

This program is made very quickly and therefore not
in any way optimized or had been thoroughly checked
for bugs. All I can say is it's very ineffecient XD

As long as its working and we can use it with the
features it currently have, I don't have plans to
improve the program at the moment.





