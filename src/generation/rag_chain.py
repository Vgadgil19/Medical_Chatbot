import sys
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR/".env")
sys.path.append(str(BASE_DIR))


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from src.Retrieval.search import ret
from langchain_chroma import Chroma
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor



llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)
model = OpenAIEmbeddings(model="text-embedding-3-small")

prompt = PromptTemplate(
    template=""" 
    You are MediRAG, an evidence-based medical information assistant.

    Your knowledge base contains medical information from indexed
    health sources.

    When users ask about your capabilities or supported topics,
    explain that you can answer questions about topics covered
    by your indexed sources.

    Do not present the retrieved documents for a general
    capability question as an exhaustive list of supported topics.

    For medical questions, answer only using the retrieved context.
    
    Answer the User Questions only based on provided context.
    Instructions:
    1. Do not introduce medical facts that are nor supported by the context.
    2. If the provided context is not sufficient for the answer, clearly say so.
    3. Explain medical terminologies in simple language.
    4. Do not skip the statistical data, medical numbers, units.
    5. Do not diagnose conditions or prescribe medications.
    6. Include the source title and URL used for your answer.
    7. Do not treat a document as sufficient evidence
       merely because it discusses a related disease or topic.

    8. If the retrieved context discusses a related condition
       but does not directly answer the question, state that
       the available sources do not provide the requested information.
    
    Context : {context},
    Question : {question}
    
    Answer : 
    """,
    input_variables=["context","question"]
    
)

vector_store = Chroma(
    collection_name="langchain",
    embedding_function=model,
    persist_directory=str(BASE_DIR/"src"/"embeddings"/"vector_db")
)

retriever = vector_store.as_retriever(search_kwargs = {"k": 3})
compressor = LLMChainExtractor.from_llm(llm=llm)
compression_ret = ContextualCompressionRetriever(
    base_retriever=ret,
    base_compressor=compressor
)

parser = StrOutputParser()

def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        content = f""" 
        Source : {doc.metadata.get('title')}
        URL : {doc.metadata.get('url')}
        Content : {doc.page_content}
        """
        formatted_docs.append(content)
    return "\n\n".join(formatted_docs)

retrieval_chain = RunnableParallel(
    {
    "context" : compression_ret | RunnableLambda(format_docs),
    "question" : RunnablePassthrough()
    }
)  

chain = retrieval_chain | prompt | llm | parser

if __name__ == "__main__":
    print("Enter the query: \n")
    query = input()
    # query = "What are the symptoms of Spinal Muscular Atropy ? "
    response = chain.invoke(query)
    print("\n MEDIRAG Response : \n")
    print(response)
    
    
    ''' 
    You are a MediRAG - A Medical Assistance Chatbot. 
    MediRAG provides evidence-based health information from its indexed medical sources. 
    It explains diseases, symptoms, prevention, and related health topics when supported by retrieved evidence.
    It does not diagnose conditions or prescribe treatments.
    It cites sources and acknowledges when information is unavailable.
    '''
    
