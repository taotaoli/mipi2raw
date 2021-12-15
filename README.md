mipir2rgb
=========

mipir2rgb 用于将mipi raw 转为 unpack raw.


Running
-------

python .\mipi2raw.py -h
	usage: mipi2raw.py [-h] [--path PATH] [--file FILE] --width WIDTH --height
					   HEIGHT --depth DEPTH

	optional arguments:
	  -h, --help       show this help message and exit
	  --path PATH      input raw path
	  --file FILE      input raw file name
	  --width WIDTH    raw image width
	  --height HEIGHT  raw image height
	  --depth DEPTH    raw image depth [8, 10, 12, 14, 16]


python .\mipi2raw.py --file .\mipiraw12_2560x1440.raw --width 2560 --height 1440 --depth 12

