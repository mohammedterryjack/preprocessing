###############################################################################################################
# COPYRIGHT (C) WLUPER LTD. - ALL RIGHTS RESERVED 2017 - Present
#
# UNAUTHORIZED COPYING, USE, REPRODUCTION OR DISTRIBUTION OF THIS FILE, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
# ALL CONTENTS ARE PROPRIETARY AND CONFIDENTIAL.
#
# WRITTEN BY:
#   Mohammed Terry-Jack <mohammed@wluper.com>
#
# GENERAL ENQUIRIES:
#   <contact@wluper.com>
###############################################################################################################
# >>>> Python Native Imports <<<<
from string import punctuation
from typing import Tuple, List
# >>>> Installed Package Imports <<<<
from num2words import num2words
from wordninja import split
from unidecode import unidecode
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
# >>>> Wluper Imports <<<<
# ==============================================================================================================
def preprocessing_pipeline(raw_string:str) -> str:
    """
    raw string: “Prease get me 2 London ,,, Bridge” 
    --> “please get me two london bridge”

        preprocessing pipeline:
            → lower case 
            → convert accented letters
            → split compounds 
            → convert numbers 
            → remove punctuation 
            → lemmatise 
    """
    lower_case_string = raw_string.lower()
    no_accents_string = convert_accented_characters(lower_case_string)
    no_compounds_string = separate_compound_words(no_accents_string)
    no_numbers_string = convert_any_numbers_to_words(no_compounds_string)
    no_punctuation_string = remove_punctuation(no_numbers_string)
    lemmatised_string = lemmatise_according_to_pos(no_punctuation_string,WordNetLemmatizer())
    return lemmatised_string


def part_of_speech_tags(raw_string:str) -> Tuple[List[str],List[str]]:
    """
    this is a test -> (
        [this,is,good],
        [noun,verb,adj]
    )
    """
    return zip(*map(
        lambda token_pos: (
            token_pos[0],
            get_wordnet_pos(token_pos[1])
        ),
        pos_tag(raw_string.split())
    ))

def lemmatise_according_to_pos(raw_string:str, lemmatiser:WordNetLemmatizer) -> str:
    """
    The stripy bats were hanging on their feet for best
    --> The strip bat be hang on their foot for best
    """
    return ' '.join(map(lemmatiser.lemmatize,*part_of_speech_tags(raw_string)))

def get_wordnet_pos(part_of_speech_tag:str) -> str:
    """
    simplify pos tags for use with wordnet lemmatiser
    default: returns Noun
    """
    return {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }.get(part_of_speech_tag[0], wordnet.NOUN)

def remove_punctuation(raw_string:str) -> str:
    """
    this-is / an ' example.com -> this is an example com
    """
    return ''.join(filter(lambda char:char not in punctuation,raw_string))

def convert_accented_characters(raw_string:str) -> str:
    """
    Málaga -> Malaga
    """
    return unidecode(raw_string)

def separate_compound_words(raw_string:str) -> str:
    """
    thisisanexample -> this is an example
    """
    return ' '.join(split(raw_string))

def keep_only_numbers(raw_string:str) -> str:
    """
    $2.00p -> 2.00
    """
    return ''.join(filter(lambda char:char.isnumeric() or char in ".,", raw_string))

def convert_numbers_to_words(raw_string:str) -> str:
    """
    pass in a string 
        - if its a number it converts it into words
        else - passes string back unchanged
    """
    try:
        return num2words(keep_only_numbers(raw_string))
    except:
        return raw_string

def convert_any_numbers_to_words(raw_string:str) -> str:
    """
    there are 300 people -> there are three-hundred people
    """
    return ' '.join(map(convert_numbers_to_words,raw_string.split()))