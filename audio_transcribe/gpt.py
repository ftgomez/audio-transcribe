import os

import openai
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


class QuestionBot:
    def __init__(self, transcript):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.transcript = transcript
        self.docsearch = None
        self.prompt_template = (
            "You are a bot that reads the transcript of an audio file and "
            "answers questions about its content. The transcript is the following: "
            + self.transcript
            + "\n{context}\nHuman: {question}\nAI:\n"
        )
        self.prompt = PromptTemplate(
            input_variables=["context", "question"], template=self.prompt_template
        )
        self.chain = load_qa_chain(
            OpenAI(temperature=0), chain_type="stuff", prompt=self.prompt
        )

    def prepare_data(self):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(self.transcript)
        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_texts(
            texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]
        ).as_retriever()
        self.docsearch.search_kwargs = {"k": 1}

    def chat(self):
        self.prepare_data()
        while True:
            query = input("Question: ")
            if query == "exit":
                print("Ending conversation")
                break
            docs = self.docsearch.get_relevant_documents(query)
            response = self.chain.run(input_documents=docs, question=query)
            print(f"Answer: {response}")

    def answer_question(self, query):
        self.prepare_data()
        docs = self.docsearch.get_relevant_documents(query)
        response = self.chain.run(input_documents=docs, question=query)
        return response

    def auto_chat(self, list_query):
        self.prepare_data()
        for i in range(len(list_query)):
            query = list_query[i]
            docs = self.docsearch.get_relevant_documents(query)
            response = self.chain.run(input_documents=docs, question=query)

        return response
