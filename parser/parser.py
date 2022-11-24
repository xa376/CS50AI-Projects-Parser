import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Not enough knowledge of english to figure out in less than 4 hours
NONTERMINALS = """
S -> NP VP

AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | N PP | NV
PP -> P NP | P Det NP
VP -> V | V NP | V NP PP | V PP | Adv V PP NP | V P Det Adj N Conj N V
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []

    # Turns sentence to lowercase, gets each word from sentence, and if word has alphabetic character
    # appends that word to words
    for word in nltk.tokenize.wordpunct_tokenize(sentence.lower()):
        for character in word:
            if character >= 'a' and character <= 'z':
                words.append(word)
                break

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # For each subtree, adds each NP labeled tree with no children to chunks, unless its already there
    for subtree in tree.subtrees():
        if subtree != tree:

            # If subtree is labeled NP assigns newchunk to be a NP without children trees
            if subtree.label() == "NP":
                newChunk = chunkReturn(subtree)

                # Appends chunk to list if not already inside it
                if newChunk not in chunks:
                    chunks.append(newChunk)

    return chunks

# Recursive function that returns a tree labeled NP with no children NP trees
def chunkReturn(tree):

    # If a subtree in the tree is labeled NP, passes that subtree back to the function
    for subtree in tree.subtrees():
        if tree != subtree:
            if subtree.label() == "NP":
                nextTree = chunkReturn(subtree)
                return nextTree
    
    # If no subtrees with NP were found returns the tree
    return tree


if __name__ == "__main__":
    main()
