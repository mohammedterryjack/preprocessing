from typing import List, Iterator

from nltk import word_tokenize, pos_tag, RegexpParser
from nltk.tree import Tree

REGEX_NP_PATTERNS= r"""
    NP: {<NN><NN>+}
        {<NNP><NNP>+}
        {<NN><VBG>+}
        {<RB><VBN>+}
        {<RB><VB>+}
        {<VBG><NN>+}
        {<ADJ><NN>+}
        {<CD><NNS>+}
"""
class Chunker(RegexpParser):
    def __init__(self) -> None:
        super().__init__(REGEX_NP_PATTERNS)

    def chunk(self, sentence:str) -> List[str]:
        tokens = word_tokenize(sentence)
        tags = pos_tag(tokens)
        tree = self.parse(tags)
        chunks = self.convert_tree_to_chunks(tree)
        return list(chunks)

    @staticmethod
    def convert_tree_to_chunks(tree:Tree) -> Iterator[str]:
        for node in tree:
            if isinstance(node,Tree):
                yield Chunker.extract_string_from_tree(node)
            else:
                yield node[0]

    @staticmethod
    def extract_string_from_tree(tree:Tree) -> str:
        return ' '.join(
            node[0] for node in tree.leaves()
        )
