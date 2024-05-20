from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
import traceback
import os

class InsightGenerator:
    def __init__(self, config):
        self.config = config
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        self.retriever = self._setup_retriever()

    def _setup_retriever(self):
        loader = DirectoryLoader(self.config['Directory'], show_progress=True)
        documents = loader.load()
        docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(documents)
        vectordb = Chroma.from_documents(documents=docs, embedding=self.embeddings, persist_directory='db')
        vectordb.persist()
        return vectordb.as_retriever(search_kwargs={"k": 2})

    def generate_insights(self, df):
        insights = {}
        llm = ChatOpenAI(temperature=0.4, model_name='gpt-3.5-turbo')

        for column in df.columns.difference(['Timestamp']):
            data_points = df[column].dropna().tolist()
            if data_points:
                prompt_template = """
                    Based on the following data for {column}:
                    - Scores: {data_points}
                    
                    Please provide empathetic insights into how this aspect affects the person's well-being, suggesting potential areas of support and improvement. Make sure there is no grammatical errors. 
                    The name given for the data is not a person its their daily need. And also use scores while generating the insights mention the numbers in content.
                """

                prompt = PromptTemplate(template=prompt_template, input_variables=["column", "data_points"])
                prompt_with_values = prompt.format(column=column, data_points=data_points)

                try:
                    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="map_reduce", retriever=self.retriever, return_source_documents=True)
                    result = qa_chain({"query": prompt_with_values})
                    insights[column] = result['result']
                except Exception as e:
                    print(f"Failed to generate insights using retrieval for {column} due to an error: {e}")
                    print(traceback.format_exc())

        return insights
