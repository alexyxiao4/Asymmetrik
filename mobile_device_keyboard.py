#!/usr/bin/env python3
# mobile_device_keyboard

import re


class AutocompleteProvider:

    def __init__(self):
        self.cand_list = []
#Return a list of Candidates sorted by highest number of repetitions when "trained"
    def get_words(self, fragment):
        to_sort = {}
        for frag in fragment:
            for cand in self.cand_list:
                if frag in cand.get_word():
                    to_sort[cand] = cand.get_confidence()
        sorted_cands = sorted(to_sort.items(), key=lambda x: x[1], reverse=True)

        temp_array = []
        for candidate in sorted_cands:
            temp_array.append(candidate[0])
        return temp_array
#counts occurnces of words to give them more "weight" when evaluating word fragments
#takes in list
    def train(self, passage):
        #every element in list, if it's already present, increment counter for the 
        #and instance var
        for text in passage:
            counter = 0
            #if word seen, increment Candidate counter and var counter
            for cand in self.cand_list:
                if text == cand.get_word():
                    cand.count += 1
                    counter += 1
            #if a new word, make a new Candidate
            if counter == 0:
                new_word = Candidate()
                new_word.word = text
                new_word.count += 1
                self.cand_list.append(new_word)


class Candidate:
    def __init__(self):
        self.word = ""
        self.count = 0

    def get_word(self):
        return self.word

    def get_confidence(self):
        return self.count


if __name__ == "__main__":
    all_words = AutocompleteProvider()
#Welcome message/commands
    help_string = "The only accepted commands are: Train: input_string, Input: string_fragment, exit, and ?"
    print(help_string)
    while True:
        user_input = input()
        if user_input == "exit":
            break
        if user_input == "?":
            print(help_string)
        split_words = user_input.split()
        #if first thing entered is Train:
        if split_words[0] == "Train:":
            #remove Train:
            new_input = user_input.replace("Train:", "")
            #remove anything except for whitespace and valid chars
            new_input = re.sub("[^\w ]", "", new_input)
            #make everything lowercase, toss in the words to be "trained"
            all_words.train(new_input.lower().split())
        elif split_words[0] == "Input:":
            #remove Input:
            new_input = user_input.replace("Input:", "")
            #make everything lowercase, push fragments and call get_words from the Auto class
            possible = all_words.get_words(new_input.lower().split())
            for part in possible:
                print(part.get_word(), "(", part.get_confidence(), "),", end = ' ')
            print("\n")
        else:
            print("Invalid command, try ? if you need the command list.")
