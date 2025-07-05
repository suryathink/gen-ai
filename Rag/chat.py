from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI


load_dotenv()
client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model='text-embedding-3-large'
)


vector_db= QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding = embedding_model
)

# Take user query
query = input("> ")



# vector similarity search [query] in DB
search_results = vector_db.similarity_search(
    query=query
)


# print("search results: ",search_results)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = """
    You are a helpful AI Assistant who answers user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only answer the user based on the following context and navigate
    the user to open the right page number to know more.

    Context: {context}

"""


# print("SYSTEM_PROMPT", SYSTEM_PROMPT.format(context=context))

chat_completion = client.chat.completions.create(
    model='gpt-4.1',
    messages=[
        {"role":"system", "content" : SYSTEM_PROMPT.format(context=context)},
        {"role":"user", "content" : query}
    ]
)

bot_icon = "🤖"

response = chat_completion.choices[0].message.content
print(f"{bot_icon  } {response}")

