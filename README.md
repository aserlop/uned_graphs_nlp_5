# UNED TextRank

## Description

Source code for the assignment of unit 5 in Graphs applied to NLP course inside the Language Technologies UNED's masters program.
The assignment consists of elaborating a program that fulfills the following functionalities given a collection of documents:
* Build a co-occurrence matrix and export it in Pajek format.
* Develop an implementation of TextRank, obtain the most relevant terms and export them in a text file.


## Instructions of use

Prerequisites:

* Conda navigator installed

Instructions:

* Clone this repository or use the zip version.
* Modify json in resources with your specific parameters
* Open a bash terminal and change directory to the bash folder
* Run `sh create_env.sh` to create an environment with the library installed
* Run `sh launch_app.sh` to run the program.

Outputs:
* File with co-occurrence matrix in Pajek format at output_base_path
* (Optional) File with the keyphrases
* Log file with all the info of the process

## Configuration

The program can be used using the json file inside the resources folder its structure is as follows:

* input_base_path (str). Path to folder containing all the documents to proccess.
* output_base_path (str). Path to folder to export all the results obtained.
* duplicated_char_list (List[str]). List of characters to preprocess an drop consecutive duplicates.
* valid_tag_list (List[str]). Valid tags to remain in each document. If empty list is given all tags are used.
* do_global (int). Can be either zero if we want to run the program treating each document separately or one if we want to combine all documents into one.
* do_textrank(int). Can be either zer if we only want to get the co-occurrence matrix and export it or one if we want to do both co-ocurrence matrix and keyphrases.
* num_tokens_window (int). Number of tokens to consider two words as a pair.
* num_keyphrases (int). Number of keyphrases to export after ranking using TextRank.
* textrank_params. Parameters of the PageRank algorithm.
    * damping (float). PageRank's damping factor, by default 0.85
    * min_diff (float). Minimun difference to pass to the next epoch.
    * num_epochs (int). Number of epochs
