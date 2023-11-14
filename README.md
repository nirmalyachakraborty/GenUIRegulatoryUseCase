# PDFExtractionLangChain
Shows how to extract PDF Contents using Langchain and Pydantic data models using Function call and OpenAI GPT. Then uses VectorDB to query PDF.<br>
The required installations are :<br>
pip install openai==0.27.8<br>
pip install pyPDF<br>
pip install faiss-gpu<br>
pip install --upgrade langchain<br>
pip install pyPDF2<br>
pip install streamlit<br>

Before running any code, use : export OPENAI_API_KEY=................ to set the env var for openai

1.To extract contents of PDF file, edit extPDF.py and update the PDF file name in the line <br>
getStructInfo("FR_Y-9C20230930_file Current.pdf",1,"CURR_JSON") -- here second parameter is number of pages to extract (starting from first), third parameter is output JSON <br>
Run : python extPDF.py
2. To query PDF, open queryPDF.py, and update the PDF file in line<br>
loader = PyPDFLoader("FR_Y-9C20230930_file Current.pdf") <br>
Update the query in the line : query = "............." <br>
Run : python queryPDF.py
3. To query PDF in interactive mode: <br>
use cmd : streamlit run chatPDF.py <br>
Upload PDF and type in the Query.



