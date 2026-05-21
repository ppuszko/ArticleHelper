from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

import base64 
import time 

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.LATEX,
)

separators=[
    "\n\\title{",
    "\n\\author{",
    "\n\\section{",
    "\n\\subsection{",
    "\n\\begin{abstract",
    "\\\n%",
    "\\\n\n%",
    "%",
    "\n\n"
]


splitter_h = RecursiveCharacterTextSplitter(
    separators=separators,
)

with open("files/arXiv-2504.03930v1/colm2025_conference.tex") as f:
    doc = f.read()

docs = splitter_h.create_documents([doc])

print(len(docs))

for i, document in enumerate(docs[:10]):

   print(f"{i}:\n{document.page_content}")

"""


    
chat = ChatOllama(model="qwen3-vl:8b", temperature=0.1)

with open("files/arXiv-2504.03930v1/plots/benchmarks_saturated.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

message = HumanMessage(
    content = [
        {
            "type": "image_url",
            "image_url": f"data:image/png;base64,{image_data}"
        },
        {
            "type": "text",
            "text": "Describe what this figure shows"
        }
    ]
)

start = time.time()
response = chat.invoke([message])
print(f"\n qwenVL: {response.content} \n meta: {response.usage_metadata}")
end = time.time()"""


"""import pymupdf 

doc = pymupdf.open("files/arXiv-2504.03930v1/2504.03930v1.pdf")

for page in doc:
    text = page.get_text()
    print(f"\n\nPage: {text}")"""