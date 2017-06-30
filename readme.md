# VeganBot : A chatty robot promoting veganism

### Requirements

- [python >= 3.4.3](https://www.python.org/downloads/release/python-343/)
- [flask](http://flask.pocoo.org/docs/0.10/installation/): `pip3 install Flask`
- [PyDictionary](https://pypi.python.org/pypi/PyDictionary/1.3.4): `pip3 install PyDictionary`

### Setup

1. Clone the repo `git clone <repo>`
2. Change directory `cd <repo>`
3. Run `python3 vegan_bot.py -h` to see how to use this program.
4. Run `python3 vegan_bot.py` plus optional arguments if desired (see bottom of this document for optional arguments).
5. Type `127.0.0.1:5000` in the address bar of your favorite browser and hit enter.
6. Have a chat with VeganBot.

### Example

Lets say:

* You wanted to have a chat with VeganBot with synonyms turned on for both user input and keyword lists.
* You wanted to see the keywords for the answer given for your input.

You could then:

* Open up a command line tool and move into the folder containing this README file.
* Run the command: `python3 vegan_bot.py -v -o -t`
* Wait a couple of minutes while VeganBot gets his keyword lists sorted out (you only have to do this once).
* Type in `127.0.0.1:5000` in the address bar of your favorite browser and hit enter.
* Have a chat with VeganBot.
* Open the file 'log.txt' (located in the working directory) to see the information you wanted.

Here are a few examples of input strings that are common justifications for harming and exploiting animals:

* It doesn't harm cows to take their milk
* It doesn't harm hens to take their eggs
* I just like the taste of bacon, it's so great
* It's just a matter of culture
* Our ancestors ate meat
* We're on top of the food chain
* It's my personal choice, I have the right to do as I wish
* It's not healthy
* But where do you get your protein?
* What about B12?
* It's too hard, I just don't have the willpower
* Vegan food tastes horrible
* Plants have feelings tho
* Stop forcing your beliefs on me!

### Additional features

#### Stem

~~The program only uses roots of the words for better comparison. This is implemented using [stemming](https://pypi.python.org/pypi/stemming/1.0).~~ Momentarily disabled

#### Synonyms

If desired, the user can give optional arguments to activate synonyms for both user input and keywords lists. This should result in better results from VeganBot, because he can understand a lot more words. However, this is not always the case, so if you get an answer unrelated to your question, try running without the synonyms. This is implemented using [PyDictionary](https://pypi.python.org/pypi/PyDictionary/1.3.4)

#### Storing dictionaries

When running with synonyms for the keyword lists, the start-up time can be a couple of minutes. To compensate, this feature was added so the user only needs to wait once, even though he runs the program several times with synonyms activated. The dictionary that resulted after finding all the synonyms was written to file in CSV form, then the program could just read that file the next time it was run, instead of generating synonyms for all the keywords again.

I suppose the CSV file could have been used to skip this waiting period altogether, but I wanted to show how the database was built, including this step.

#### Commons

Common words that do not give any clues about what topic the user is talking about are removed from the equation when trying to figure out the topic. This is implemented using Counter from collections.

#### Optional arguments

* `-v` or `--key`: Prints to logfile the key that had the most hits, the number of most hits and the list of keywords for that key, along with the user input
* `-e` or `--justifications`: Prints to logfile the justifications list
* `-g` or `--justifications-dict`: Prints to logfile the justifications dictionary
* `-a` or `--answers`: Prints to logfile the answers list
* `-n` or `--answers-dict`: Prints to logfile the answers dictionary
* `-b` or `--commons`: Prints to logfile the commons list
* `-o` or `--synonyms`: Turns on synonyms for keyword lists. 
  - WARNING: Takes a while to start up the program for the first time (couple of minutes).
* `-t` or `--synonyms-input`: Turns on synonyms for user input. 
  - WARNING: Replies from the bot might take a bit longer (never more than a few seconds though).

Most of these arguments were added to make it easier to figure out what's going on in the code quickly. 

The first one though, `-v` helps you see what keywords were matched in the selected answer. So, f.ex. if you got an answer that was not on your topic, you could try a rephrase without those words that were matched in the unwanted answer.

The last two were added to make it possible for the user input to have a variety of words with same meaning, but still being able to find the correct topic, using synonyms. `-o` adds synonyms of each word in the keylist, and `-t` adds synonyms of each word in the user input. Obviously this slows down the program quite a bit, especially the startup time with `-o`, but thankfully, you only have to wait the one time!

### For the future

I intend to take this project further during the summer, so when testing this program, it would be greatly appreciated to always run with `-v` (at least) and when you're finished, email me the logfile ('log.txt') at atlisg12@ru.is. That way, I can see how the VeganBot responded to your questions and statements, thus improving the program based on some actual data. Of course, the next step would be to try implementing some actual AI so that VeganBot can learn by himself and improve on his own.

##### Footnote: The data used for the database was taken from [here](http://www.vegansidekick.com/guide).
