from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader

def getText(file_path):
    loader = PyPDFLoader(file_path)

    documents = loader.load()
    text = ""
    for doc in documents:
        text += doc.page_content
    return text

with open('CURR_old.txt') as f:
    lines = f.readlines()
CURR_DOC = " ".join(lines)


with open('OLD_old.txt') as f:
    lines = f.readlines()
OLD_DOC = " ".join(lines)

CURR_DOC = getText("FR_Y-9C20230930_file Current.pdf")

OLD_DOC = getText("FR_Y-9C20230630_file_June.pdf")

docs = f""""
CURRENT_FILE_EXTRACT={CURR_DOC}

OLD_FILE_EXTRACT={OLD_DOC}
"""

print(docs[:5000])

model = ChatOpenAI(model_name="gpt-3.5-turbo-16k",temperature=1.2,max_tokens=4000)

template_string = """Find the difference in the financial terms in the reports \
that is given by CURRENT_FILE_EXTRACT and OLD_FILE_EXTRACT from the same keys and using the values\
For example give the change in the values of similar keys in two reports, do not calculate, just give the two values and highlight the differences
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

rpt_messages = prompt_template.format_messages(
                    text=docs)

rpt_response = model(rpt_messages)

print(rpt_response.content)