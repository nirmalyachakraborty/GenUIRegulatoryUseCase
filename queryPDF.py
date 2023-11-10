from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader


def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=3000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = OpenAIEmbeddings()
    knowledgeBase = FAISS.from_texts(chunks, embeddings)

    return knowledgeBase

def process_pages(pages):

    embeddings = OpenAIEmbeddings()
    knowledgeBase = FAISS.from_documents(pages, embeddings)

    return knowledgeBase

model = ChatOpenAI(model_name="gpt-4-32k", temperature=1.2, max_tokens=4000)

loader = PyPDFLoader("FR_Y-9C20230930_file Current.pdf")
    #"FR_Y-9C20230630_file_June.pdf")
#FR_Y-9C20230930_file Current


documents = loader.load()
text = ""
for doc in documents:
    text += doc.page_content

#pages = loader.load_and_split()

knowledgeBase = process_text(text)
    #process_pages(pages)
    #process_text(text)

print("knowledge base created")

query = "How many MAIN schedules are there in the document , Name the main Schedules with description?"
    #"What is the rule for Derivative Contracts in Schdule HC-N and what is the fair value (unit in Billion dollars)"
    #"What is total interest income and Total Interest Expense, with full details. Consider the unit as Billion Dollars?"
    #"What is the total assets adn total trading assets of Holding Companies for which Memorandum items 9.a through 9.e are to be completed. Answer in full. Consider only 9a through 9e"
    #"How many MAIN schedules are there in the document , Name the main Schedules with description?"
    #"How many times the word BHCK occurs in the entire document, including all schedules ?"
    #"How many times does BHCK occur in the document ?"
    #"How many schedules are there in the document ?"
    #"What is the total assets adn total trading assets of Holding Companies for which Memorandum items 9.a through 9.e are to be completed. Answer in full. Consider only 9a through 9e"
    #"What is the income and fees from the printing and sale of checks?"

docs = knowledgeBase.similarity_search(query)

llm = OpenAI()
chain = load_qa_chain(llm, chain_type='stuff')
response=""
with get_openai_callback() as cost:
    response = chain.run(input_documents=docs, question=query)
    print(cost)

print(response)


