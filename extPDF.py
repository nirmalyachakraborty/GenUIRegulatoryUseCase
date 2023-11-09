import openai
from typing import List
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from typing import Optional
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda
import json



class ScheduleInfo(BaseModel):
    """Information about Financial Schedule mentioned."""
    key: str
    value: Optional[str]

# class Overview(BaseModel):
#     """Overview of a section of text."""
#     summary: str = Field(description="Provide a concise summary of the content.")
#     keywords: str = Field(description="Provide keywords related to the content.")

class Schedule(BaseModel):
    """Information about Schedule in the report"""
    schedules: List[ScheduleInfo]

# overview_tagging_function = [
#     convert_pydantic_to_openai_function(Overview)
# ]

# summary_model = model.bind(
#     functions=overview_tagging_function,
#     function_call={"name":"Overview"}
# )
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Extract the relevant information as summary in one paragraph. Extract the keywords "),
#     ("human", "{input}")
# ])
# summary_chain = prompt | summary_model | JsonOutputFunctionsParser()
#
# print(summary_chain.invoke({"input": page_content_inp}))

schedule_tagging_function = [
    convert_pydantic_to_openai_function(Schedule)
]

template = """A financial report will be passed to you. Extract from it the schedule info as key value pairs. 
Do not consider the Item number as key, read the key description as key, and the value in the table as value.
Use the numeric or alphanumeric value as value only, do not add the item number as value.
Do not make up or guess ANY extra information."""



def getStructInfo(file_path,no_pages):
    """Get the structure of the financial report.
    Parameters
    ----------
    file_path : str
        Path to the financial report.
    no_pages : int
        Number of pages to extract.
    Returns
    -------
    List[Schedule]
        List of schedules extracted from the financial report.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print("Document has :" + str(len(documents)) + " pages")

    # Do not consider the Item number as key, read the key description as key, and the value in the table as value.
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}")
    ])

    model = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=1.2, max_tokens=2000)
    # model_kwargs={'top_p':0.5}

    extraction_model = model.bind(
        functions=schedule_tagging_function,
        function_call={"name": "Schedule"}
    )

    jsonCurr=[]
    text = ""
    ctr = 0
    for doc in documents[:no_pages]:
       print("EXTRACTING INFO FROM ###############  PAGE ######################################### " + str(ctr))
       text += doc.page_content
       ctr+=1
       extraction_chain = prompt | extraction_model | JsonOutputFunctionsParser()
       jsonDoc = extraction_chain.invoke({"input": doc.page_content})
       json.dumps(jsonCurr.append(jsonDoc))
    return jsonCurr, text


CURR_DOC, CURR_DOC_TXT = getStructInfo("FR_Y-9C20230930_file Current.pdf",7)

CURR_DOC_STR=" ".join(map(str,CURR_DOC))

with open("CURR_JSON.txt", "w") as outfile:
    outfile.write("".join(CURR_DOC_STR))

with open("CURR_TEXT.txt", "w") as outfile:
    outfile.write(CURR_DOC_TXT)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

OLD_DOC, OLD_DOC_TXT = getStructInfo("FR_Y-9C20230630_file_June.pdf",7)
OLD_DOC_STR=" ".join(map(str,OLD_DOC))

with open("OLD_JSON.txt", "w") as outfile:
    outfile.write("".join(OLD_DOC_STR))

with open("OLD_old.txt", "w") as outfile:
    outfile.write(OLD_DOC_TXT)


