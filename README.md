# Keyboard layout evaluation

An evaluation of existing keyboard layouts in order to choose one for my use.

The goal is to compare keyboard layouts for an ergonomic keyboard, for several languages. 
The first step is to gather statistics of characters use for each language; then to implement a method to compare them according to subjective criterias.

The evaluation method relies on grading bigrams according to weights per key and penalties, and applying over bigram frequencies for a language.

# Table of contents

- [Keyboard layout evaluation](#keyboard-layout-evaluation)
- [Table of contents](#table-of-contents)
- [Character statistics](#character-statistics)
  - [Count script](#count-script)
  - [Spreadsheet analysis](#spreadsheet-analysis)
    - [Character counts](#character-counts)
    - [Bigram counts](#bigram-counts)
  - [Takeaway](#takeaway)
- [Layout evaluation](#layout-evaluation)
  - [Principle](#principle)
  - [Script](#script)
  - [Results](#results)
- [Conclusion](#conclusion)

# Character statistics

Contained in folder `character_stats`.

The [layout evaluation](#layout-evaluation) needs bigram frequencies (sets of 2 letters), for each language.

The frequencies are sourced from the literature [here](http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/). I focused on English, French, Spanish, and German. 

For comparison my own corpus is also analysed (for English and French); made of my emails, some texts from free books, and some internet articles.

## Count script

Requirements: Python 3, Pandas.

The script `count.py` takes the text files in the `data` folder and outputs the character counts in `chars.csv`, and the bigram counts in `bigrams.csv`. Upper case are converted to lower case.

The list of characters to take into account is configurable in the code, in the list `chars`. Currently it takes the basic alphabet, plus `éèêàçâîô.,-'/`. 

The provided `chars.csv` and `bigrams.csv` files were generated with a personal corpus of emails (`mails_en` and `mails_fr`, 300\~400kB of raw text each) and various free books and articles (`vrac_en` and `vrac_fr`, 200\~400kB each).

## Spreadsheet analysis

This analysis is done in the Libreoffice spreadsheet `stats.ods`.

### Character counts

The characters frequencies for both English and French are quite consistent between the "theory" and my own corpus.

![chars_en](images/chars_en.png "Character occurences in corpus, English")

![chars_fr](images/chars_fr.png "Character occurences in corpus, French")

### Bigram counts

The bigram counts show some fairly large discrepancies however. The charts below show the top 80 bigrams. 

![bigram_en](images/bigram_en.png "Bigram occurences in corpus, English")

![bigram_fr](images/bigram_fr.png "Bigram occurences in corpus, French")

## Takeaway

For the evaluation, the "theory" numbers will be used, but this shows that the results should be taken with a big grain of salt. 

Additionally the "theory" numbers do not contain characters such as `.,-'/`.

Small differences of grades between layouts won't be conclusive. The analysis should be understood as making a rough estimation of value between layouts, not a precise assessment.

# Layout evaluation

Contained in folder `layout_evaluation`.

## Principle

TODO

## Script

Requirements: Python 3, Pandas, Matplotlib.

The script `script.py` uses the bigram statistics from `stats.csv`, and the configuration (key weights, penalties, and layouts definitions) from `config.txt` to generate the results (table and plot).

The code isn't very efficient as it iterates through dataframes to generate the results. It executes in \~10s so in practice it doesn't really matter.

## Results

TODO

![results](images/results.png "Grades per layout")

Layout|English|French|Spanish|German
--|--|--|--|--
MTGAP 2.0|307.988|304.948|301.514|301.202
MTGAP "ergonomic"|312.957|320.791|308.714|309.736
Colemak DHm|317.330|315.008|309.139|310.236
MTGAP|317.761|327.706|318.726|315.139
MTGAP "shortcuts"|319.120|320.483|303.471|304.363
MTGAP "standard"|321.019|318.934|308.401|313.419
Workman|321.197|340.442|328.652|318.544
Colemak DH|324.259|325.342|319.388|315.181
Kaehi|325.659|330.745|325.707|324.158
MTGAP "Easy"|325.875|320.665|311.27|304.329
Colemak|327.508|316.784|313.226|323.361
Oneproduct|327.802|353.749|337.753|329.509
Norman|333.891|351.450|348.196|332.151
ASSET|340.265|326.668|323.568|337.202
BEAKL|342.748|353.122|342.994|352.317
qgmlwyfub|346.455|362.024|349.379|345.063
Carpalx|347.630|364.385|352.467|356.831
Qwpr|349.765|342.349|332.947|341.037
Minimak-8key|356.441|351.66|349.038|356.164
Bépo 40%|358.328|319.911|335.219|344.977
Coeur|366.680|326.857|332.814|345.738
Dvorak|371.568|378.151|375.557|361.538
Neo|375.679|360.455|363.138|341.696
Qwertz|498.357|483.748|467.192|480.146
Qwerty|501.407|487.751|459.333|485.922
Azerty|541.837|518.064|518.258|505.143


# Conclusion

TODO