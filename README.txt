Hello!
This is my mini-project analyzing option volume for China's A-Share ETF call and put options.

I initially became interested in China's A-Share ETF market when I analyzed its movement during a college internship. After my internship, I wanted to see if I could create a small-scale trading strategy using price data, options data, and various other signals from this ETF as well as other Asian stocks & derivatives. 
This repository was my first attempt at interpreting the options data I collected. Note, the rest of my project is not included as I still use some of the strategies in my personal investments today!

main.py is main program that reads the data file, interprets the data, and presents the relevant findings.
data.py contains three classes (Data, Option, and DataSet) that support the reading and analysis of the options data.
Options.zip includes a portion of the option data I collected, in the format that data.py can read
