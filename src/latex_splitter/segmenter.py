from src.latex_splitter.schemas import DocSegment, LatexSeparators

separators =  ["\\title{", "\\author{", "\\section{", 
               "\\subsection{", "\\begin{figure}", 
               "\\begin{abstract}", "%"]

class Segmenter:
    def __init__(self, separators: list[str] = separators):
        self._separators = separators
        self._sep_lens = [len(sep) for sep in self._separators]
        self._max_sep_len = max([len(sep) for sep in self._separators])
        self._segments: list[DocSegment] = []
    

    def _find_next_separator(self, text: str, start: int, separators: list[str]) -> tuple[int, str, int] | None:
        earliest = None 
        for sep in separators:
            idx = text.find(sep, start)
            if idx != -1:
                if earliest is None or idx < earliest[0]:
                    earliest = (idx, sep, idx + len(sep))
        return earliest

    def create_segments(self, text: str):
        self._segments = []
        position = 0

        while position < len(text):    
            next_sep = self._find_next_separator(text, position, self._separators)
            if next_sep is None:
                break
            
            if len(self._segments) > 0:
                if self._segments[-1].content in ["", " ", "\n", "\n\n", "\n\n\n"]:
                    self._segments.pop()
                else:
                    self._segments[-1].content = text[position:next_sep[0]]
            
            position = next_sep[2]
            if next_sep[1] == LatexSeparators.COMMENT.value:
                next_sep = self._find_next_separator(text, position, ["\n"])
                if next_sep is None:
                    break
                position = next_sep[2]
            self._segments.append(DocSegment(type=LatexSeparators(next_sep[1])))
        
        self._segments[-1].content = text[position:]
        return self._segments
    


