#!/usr/bin/python3
import sys, json

"""
parse_json - Takes in a string containing a sequence of well formed json objects and returns a generator object of the json objects parsed.

Parameters:

word: str - String containing a sequence of well formed json objects

Output -> Generator object containing all parsed json objects
    Throws ValueError when invalid json is provided to raw_decode()
"""
def parse_json(data: str):
    decoder = json.JSONDecoder()
    ##Strip whitespace from left side
    clean_data = data.lstrip()
    while clean_data:
        try:
            val, new_idx = decoder.raw_decode(clean_data, idx=0)
        except json.JSONDecodeError as e:
            raise ValueError("Unable to parse json. Please verify that the provided string is well formed JSON.")
        ##Set clean_data to everything after the latest index read
        clean_data = clean_data[new_idx:].lstrip()
        return val