from langchain.chains.summarize.chain import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = Ollama(model="llama3.1", temperature=0.0)

CHUNK_TEMPLATE = "You are given a part of dialog from fictional characters. Please provide a list of topics discussed in the dialog, keep it concise and lean. Text is in Ukrainian or Russian, when extracting topics keep the original language. Messages: \n\n {text}"
map_prompt = PromptTemplate(input_variables=["text"], template=CHUNK_TEMPLATE)

FINAL_COMBINE_TEMPLATE = "Please provide a final summary of unique topics discussed in the form of bullet point list, keep the original language of topics. \n {text}"
combine_prompt = PromptTemplate(input_variables=["text"], template=FINAL_COMBINE_TEMPLATE)


def format_messages_for_llm(chat_messages: list):
    formatted_messages = "#| \n".join(
        f"Message#{message['id']} by {message["sender_id"]}: {message["message"]}" for message in chat_messages
    )

    return formatted_messages


def get_chunked_documents(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=50, separators=["#|", " ", ".", ","]
    )
    chunked_documents = text_splitter.create_documents([text])
    for i, chunk in enumerate(chunked_documents):
        print(f"Chunk {i+1} length: {len(chunk.page_content)}")

    return chunked_documents


def summarize_topics(messages: list) -> list:
    formatted_messages = format_messages_for_llm(messages)

    chunks = get_chunked_documents(formatted_messages)
    chunks_list = [chunks]

    if len(chunks) > 10:
        chunks_list = [chunks[i : i + 5] for i in range(0, len(chunks), 5)]

    print(f"Total chunk sublists: {len(chunks_list)}")
    final_res = ""
    for i, chunks in enumerate(chunks_list):
        print(f"Processing chunk sublist {i+1} of {len(chunks_list)}. Chunk length: {len(chunks)}")

        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt,
            verbose=False,
            map_reduce_document_variable_name="text",
            combine_document_variable_name="text",
        )
        partial_res = summary_chain.run(chunks)
        final_res += partial_res
    return final_res
