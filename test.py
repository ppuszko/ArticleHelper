from src.latex_splitter.segmenter import Segmenter

from src.latex_splitter.schemas import LatexSeparators

seg = Segmenter()

with open("files/arXiv-2504.03930v1/colm2025_conference.tex") as f:
    doc = f.read()




res = seg.create_segments(doc)

for i, r in enumerate(res[:60]):
    """if (r.type == LatexSeparators.FIGURE 
        or r.type == LatexSeparators.AUTHOR 
        or r.type == LatexSeparators.ABSTRACT 
        or r.type == LatexSeparators.SECTION
        or r.type == LatexSeparators.SUBSECTION):"""
    print(f"type: {r.type.name}, \ncontent: {r.content}")


print(len(res))
