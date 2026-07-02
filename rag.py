from langchain_community.document_loaders import PyPDFLoader
import os 
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate


#here we are setting the envi 
load_dotenv()
api_key= os.getenv("GROQ_API_KEY")

#loading
find_path =  PyPDFLoader("data/example.pdf") #building
loaded = find_path.load()

#splitting
text_splitter = RecursiveCharacterTextSplitter( #building 
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(loaded)

#embedding + storing
embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2") #building the tool



if os.path.exists("index/faiss_index"): #check if teh FAISS is already done and stored in a folder
    vectorestore = FAISS.load_local("index/faiss_index",embeddings,allow_dangerous_deserialization=True) #if already done just load the embedding / the second argument is to know which embedding used in teh prompt
    print("Loaded existing index")
else:
    vectorestore = FAISS.from_documents(chunks,embeddings) #lists of document objects
    vectorestore.save_local("index/faiss_index")
    print("Built and saved new index")

#call teh llm

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=api_key
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Use only the context below to answer.
If unsure, say "I don't know based on the document."
Context: {context}
Question: {question}
Answer:"""
)

#search relevant things
retriever = vectorestore.as_retriever(search_kwargs={"k":3})
query = "Who is the governor of Zorvath?"

docs = retriever.invoke(query) #searches to the vectorestore for the closest matching vector after embedding it 

context = "\n\n".join([doc.page_content for doc in docs])

#generate final prompt and sends to llm
final_prompt = prompt.format(context=context, question=query)


answer = llm.invoke(final_prompt)
print(answer.content)








