from pathlib import Path
import os
import traceback

import docx2txt
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


ANSWER_PROMPT = PromptTemplate.from_template(
    """Use the following reference material to answer the request.

Reference material:
{context}

Request:
{question}
"""
)


class InsightGenerator:
    def __init__(self, config):
        self.config = config
        self.embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
        self.retriever = self._setup_retriever()

    def _load_documents(self):
        documents = []
        for path in sorted(Path(self.config['Directory']).glob('**/*.docx')):
            text = docx2txt.process(str(path))
            if text and text.strip():
                documents.append(Document(page_content=text, metadata={"source": str(path)}))
        return documents

    def _setup_retriever(self):
        documents = self._load_documents()
        docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(documents)
        # Chroma persists to persist_directory automatically.
        vectordb = Chroma.from_documents(documents=docs, embedding=self.embeddings, persist_directory='db')
        return vectordb.as_retriever(search_kwargs={"k": 2})

    def generate_insights(self, df):
        insights = {}
        llm = ChatOpenAI(temperature=0.4, model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'))
        chain = ANSWER_PROMPT | llm | StrOutputParser()

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
                    source_docs = self.retriever.invoke(prompt_with_values)
                    context = "\n\n".join(doc.page_content for doc in source_docs)
                    insights[column] = chain.invoke({"context": context, "question": prompt_with_values})
                except Exception as e:
                    print(f"Failed to generate insights using retrieval for {column} due to an error: {e}")
                    print(traceback.format_exc())

        return insights
