from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI

with open('CURR.txt') as f:
    lines = f.readlines()
CURR_DOC = " ".join(lines)


with open('OLD.txt') as f:
    lines = f.readlines()
OLD_DOC = " ".join(lines)

docs = f""""
CURRENT_FILE_EXTRACT={CURR_DOC}

OLD_FILE_EXTRACT={OLD_DOC}
"""

print(docs)

model = ChatOpenAI(model_name="gpt-3.5-turbo-16k",temperature=1.2,max_tokens=2000)

template_string = """Find the difference in the financial terms in the reports \
that is given by CURRENT_FILE_EXTRACT and OLD_FILE_EXTRACT. \
For example give the change in the values of similar keys in two reports, do not calculate, just give the two values and highlight the differences
"""

from langchain.prompts import ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(template_string)

rpt_messages = prompt_template.format_messages(
                    text=docs)

rpt_response = model(rpt_messages)

print(rpt_response.content)