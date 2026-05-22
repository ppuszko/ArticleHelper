from tools.schemas import DocSegment, LatexSeparators

separators =  ["\\title{", "\\author{", "\\section{", 
               "\\subsection{", "\\begin{figure}", 
               "\\begin{abstract}", "%"]

class Segmenter:
    def __init__(self, separators: list[str] = separators):
        self._separators = separators
        self._segments: list[DocSegment] = []

    def create_segments(self, text: str):
        position = 0

        while position < len(text):    
            next_sep = self._find_next_separator(text, position, self._separators)
            if next_sep is None:
                break
            
            if len(self._segments) > 0:
                if text[position:next_sep[0]] in ["", " ", "\n", "\n\n", "\n\n\n"]:
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
    
    def get_fig_paths(self, text: str, start: int = 0) -> list[str]:
        paths = []

        plot = self._find_next_separator(text, start, ["\\begin{tikzpicture}"])
        if plot is not None:
            start = plot[2]
            plot_end = self._find_next_separator(text, start, ["\\end{tikzpicture}"])
            if plot_end is not None:
                paths.append(text[start:plot_end[0]])
        else:
            while True:
                fig_sep = self._find_next_separator(text, start, ["\\includegraphics"])
                if fig_sep is None:
                    break
                
                start = fig_sep[2]
                bracket = self._find_next_separator(text, start, ["]"])
                open_brace = self._find_next_separator(text, start, ["{"])
                if open_brace is None:
                    break
                if bracket is not None:
                    if bracket[2] < open_brace[2]:
                        start = open_brace[2]
                    else:
                        open_brace = self._find_next_separator(text, bracket[2], ["{"])
                        if open_brace is None:
                            break
                start = open_brace[2]
                
                close_brace = self._find_next_separator(text, start, ["}"])
                if close_brace is None:
                    break
            
                paths.append(text[open_brace[2]:close_brace[0]]) 
                start = close_brace[2]

        return paths
    
    def get_marker_name(self, text: str, start: int = 0) -> str:
        close_brace = self._find_next_separator(text, start, ["}"])
        if close_brace is None:
            raise RuntimeError(f"Given text does not contain latex marker residuals. Text: {text}")
        return text[:close_brace[0]]


    def _find_next_separator(self, text: str, start: int, separators: list[str]) -> tuple[int, str, int] | None:
        earliest = None 
        for sep in separators:
            idx = text.find(sep, start)
            if idx != -1:
                if earliest is None or idx < earliest[0]:
                    earliest = (idx, sep, idx + len(sep))
        return earliest


