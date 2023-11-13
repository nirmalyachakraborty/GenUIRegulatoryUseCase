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


class Schedule(BaseModel):
    """Information about Schedule in the report"""
    pageNumber: str = Field(description="Provide the page number.")
    scheduleName: str = Field(description="Provide the Schedule name.")
    schedules: List[ScheduleInfo]



schedule_tagging_function = [
    convert_pydantic_to_openai_function(Schedule)
]

template = """A financial report will be passed to you. Extract from it the schedule info as key value pairs with the schedule description as schedule name. 
Do not consider the Item number as key, read the key description as key, and the value in the table as value.
Use the numeric or alphanumeric value as value only, do not add the item number as value. If the value is not present, then use "N/A" as value.
Create proper Json with double quotes.
Do not make up or guess ANY extra information."""



def getStructInfo(file_path,no_pages,json_file_name):
    """Get the structure of the financial report.
    Parameters
    ----------
    file_path : str
        Path to the financial report.
    no_pages : int
        Number of pages to extract.
    json_file_name: str
        Path to the output json.
    """
    print(file_path)
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print("Document has :" + str(len(documents)) + " pages")

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}")
    ])

    model = ChatOpenAI(model_name="gpt-4", temperature=1.8,max_tokens=4000,model_kwargs={'top_p':0.5} )
    # model_kwargs={'top_p':0.5}

    extraction_model = model.bind(
        functions=schedule_tagging_function,
        function_call={"name": "Schedule"}
    )

    ctr = 0
    #iterate through the document array and for each page, extract the JSON info and write to a file
    for doc in documents[:no_pages]:
       print("EXTRACTING INFO FROM ###############  PAGE ######################################### " + str(ctr))
       #print(doc.page_content)
       ctr+=1
       extraction_chain = prompt | extraction_model | JsonOutputFunctionsParser()
       jsonDoc = extraction_chain.invoke({"input": doc.page_content})

       file_path = json_file_name+str(ctr)+".json"
       with open(file_path, "w") as outfile:
           outfile.write(json.dumps(jsonDoc))

       print("written file:"+file_path)

    return


getStructInfo("FR_Y-9C20230930_file Current.pdf",1,"CURR_JSON")
getStructInfo("FR_Y-9C20230630_file_June.pdf",1,"OLD_JSON")






