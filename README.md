# Weekly update
This project is about exploiting implicit biases in the text of judicial opinions.

## Mar. 15th

The goal of this week is to replicate the from the paper: *Semantics derived automatically from language corpora necessarily contain human biases* using word vectors trained using GloVe project. 

## April 4th

The goal of this week is to calculate weat score for each judge and on multiple IAT sets. 


# File Structure
```
|-- cleaned                                   ## cleaned text data from 1880 to 2013
|   |-- 1880.zip 
|   |-- ...zip
|   `-- 2013.zip
|-- data
|   |-- BloombergVOTELEVEL_Touse.dta          ## vote level data
|   `-- glove.840B.300d.txt                   ## GloVe word vectors
|-- result-score
|   `-- weat-res-type                         ## weat score for each judge corresponding to a specific IAT set (type)
|-- target-attr-words                         ## IAT set including target words and attribute words lists
|   |-- attribute_a-type
|   |-- attribute_b-type
|   |-- target_words_x-type
|   |-- target_words_y-type
|   `-- stimuli-set-type
|-- tmp                                       ## trained models
|   |-- judge_correspond_case.csv             ## judge name and corresponding case id list csv file
|   |-- judges_list.csv                       ## judge name list csv file
|   |-- model-1980
|   |-- model-[JUDGE_NAME]
|   `-- model-all
|-- README.md
|-- WEFAT.py                                  ## code for calculating weat and wefat score
|-- WEFAT_Judge.py                            ## code for traning model 
`-- WEFAT_judge_by_judge.py                   ## code for training model and calcualting scores for each judge

```
