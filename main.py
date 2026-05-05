import os
import fitz 
# The Fix:
if not hasattr(fitz, "fitz"):
    fitz.fitz = fitz

from synthesizer import synthesize


def main():
    query=input("Enter your query:")
 
    result=synthesize(query)
    print(result)
    
   

main()
