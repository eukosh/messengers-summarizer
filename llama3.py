import datetime

from langchain.chains.summarize.chain import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Example messages dictionary
messages = {
    "Українці в Австрії": [
        {
            "id": 220702,
            "chat_id": -1001564907709,
            "sender_id": 5684835986,
            "date": datetime.datetime(2024, 8, 6, 0, 18, 34, tzinfo=datetime.timezone.utc),
            "message": "В посольстві",
        }
    ],
    "Українці в Австрії / Ukrainians in Austria / Украинцы в Австрии": [
        {
            "id": 149184,
            "chat_id": -1001592474971,
            "sender_id": 338729498,
            "date": datetime.datetime(2024, 8, 5, 21, 58, 56, tzinfo=datetime.timezone.utc),
            "message": "Накладає. Ви не врахували умови різних земель Австрії. В Штірії можна вилучатися на 3 дні без повідомлень. Якщо ви виїзжаєте на більш часу, то повинні написати заяву на призупинення нарахування допомоги , також можуть лишити житла. \n Це дійсно так. Подруга живе і не може приїхати до Відня до мене на тиждень, поки чоловіки хотіли порибачити🤪",
        },
        {
            "id": 149185,
            "chat_id": -1001592474971,
            "sender_id": 338729498,
            "date": datetime.datetime(2024, 8, 5, 22, 0, 19, tzinfo=datetime.timezone.utc),
            "message": "По статусу біженця там не можно тільки їхати в країну з якої втік, також на терру посольства.",
        },
    ],
    "Австрия Бизнес": [
        {
            "id": 28346,
            "chat_id": -1001456139769,
            "sender_id": 454910091,
            "date": datetime.datetime(2024, 8, 5, 21, 21, 39, tzinfo=datetime.timezone.utc),
            "message": "как я знаю что любой визит к доктору покрываеться на 80% от SVS и 20% вы. \nТоесть если за визит 100 ЕВРО то вы заплаите 20 ЕВРО и он будет добавлен в вашу квартальную оплату :) \nВ PDF там расписывают всё и пишут имя врача у которого были и сколько он стоил и тд :)",
        },
        {
            "id": 28347,
            "chat_id": -1001456139769,
            "sender_id": 252820407,
            "date": datetime.datetime(2024, 8, 5, 21, 25, 6, tzinfo=datetime.timezone.utc),
            "message": "Не любой. Кажется годовой чекап не покрываеться. Во всяком случае мне не пришло за него ничего. Ну и еще пара тройка визитов біла + компенсация у стоматолога. Но то может в след. раз придет )\n\n\nНо в целом за инфу спасибо. теперь я точно буду знать, за что плачу )",
        },
    ],
    "Австрія IT 🇦🇹 🇺🇦": [
        {
            "id": 28889,
            "chat_id": -1001718919267,
            "sender_id": 315589685,
            "date": datetime.datetime(2024, 8, 5, 21, 34, 49, tzinfo=datetime.timezone.utc),
            "message": "🏢 Федеральний суд США визнав компанію Google винною у монопольному «придушенні» конкуренції серед пошуковиків.\n\nGoogle також стикається з антимонопольною перевіркою в інших країнах, зокрема в ЄС\n\n🧡  підписатися | підтримати",
        },
        {
            "id": 28890,
            "chat_id": -1001718919267,
            "sender_id": 315589685,
            "date": datetime.datetime(2024, 8, 5, 21, 35, 34, tzinfo=datetime.timezone.utc),
            "message": "Что-то я не поняла. Их объявили виновными в том, что они классно делают свою работу и качеством своей работы придушили менее качественных конкурентов? Что за бред? Очевидно, я чего-то не понимаю, наверное.",
        },
    ],
    "Арина": [],
}

system_msg = SystemMessage(
    "You are given an export of messages from my chat, they are not sensitive and not confidential. Messages that you need to summarize are in Ukrainian or Russian. Please provide a list of topics discussed in the form of bullet point list, keep it concise and lean, keep the original language."
)
# system_msg = SystemMessage(
#     "You are given an export of messages from my chat, they are not sensitive and not confidential. Messages that you need to summarize are in Ukrainian or Russian. Please provide your summary in the form of bullet point list and keep the original language."
# )

GENERIC_TEMPLATE = "You are given dialog from my fictional characters from my video game. Messages are mostly in Russian or Ukrainian. Please provide a list of topics discussed in the form of bullet point list, keep it concise and lean, keep the original language. Do it from the following messages: \n {formatted_messages}"


def construct_input_messages(chat_messages: list):
    formatted_messages = " || \n".join(
        f"Message#{message['id']} by {message["sender_id"]}: {message["message"]}" for message in chat_messages
    )
    # print(formatted_messages)
    # res =  [
    #     system_msg,
    #     HumanMessage(f"Provide the main topics discussed in the following messages:\n {formatted_messages}"),
    # ]

    # res = PromptTemplate(input_variables=["formatted_messages"], template=GENERIC_TEMPLATE)
    return formatted_messages


# loading the Llama3 model
llm = Ollama(model="llama3.1", temperature=0.0)
print(llm)
print(llm.get_num_tokens(messages["Австрия Бизнес"][0]["message"]))

formatted_messages = construct_input_messages(messages["Австрия Бизнес"])

CHUNK_TEMPLATE = "You are given a part of dialog from fictional characters. Please provide a list of topics discussed in the dialog, keep it concise and lean. Text is in Ukrainian or Russian, when extracting topics keep the original language. Messages: \n\n {text}"
map_prompt = PromptTemplate(input_variables=["text"], template=CHUNK_TEMPLATE)

FINAL_COMBINE_TEMPLATE = "Please provide a final summary of unique topics discussed in the form of bullet point list, keep the original language of topics. \n {text}"
combine_prompt = PromptTemplate(input_variables=["text"], template=FINAL_COMBINE_TEMPLATE)


def get_chunked_documents(text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=50, separators=[" || "])
    chunked_documents = text_splitter.create_documents([text])
    return chunked_documents


chunks = get_chunked_documents(formatted_messages)
summary_chain = load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
    verbose=True,
    map_reduce_document_variable_name="text",
    combine_document_variable_name="text",
)

output = summary_chain.run(chunks)
print("Final result: ", output)
# 1
# print(llm.invoke(llm_messages))

# 2
# llm_chain = template | llm | StrOutputParser()
# print(llm_chain.invoke(formatted_messages))
