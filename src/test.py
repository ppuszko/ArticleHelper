from tools.segmenter import Segmenter
from tools.text_processor import TextProcessor
from tools.paper_processor import PaperProcessor
from tools.image_processor import ImageProcessor

from tools.schemas import LatexSeparators

seg = Segmenter()
tp = TextProcessor()
ip = ImageProcessor()

pp = PaperProcessor(seg,ip,tp)

res = pp.process_paper("files/colm2025_conference.tex")

for r in res:
    print(f"section: {r.section} \nsummary: {r.summary} \ncontent: {r.translated_content[:200]}\n")

"""
with open("files/colm2025_conference.tex") as f:
    text = f.read()


docs = seg.create_segments(text)
temp = {}
for doc in docs:
    if doc.type == LatexSeparators.AUTHOR:
        temp["author"] = doc.content
    if doc.type == LatexSeparators.TITLE:
        temp["title"] = doc.content

print(tp.infer_authors(temp["author"], temp["title"]))"""

