from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

class InsightsGenerator:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(temperature=0.4, model_name='gpt-3.5-turbo')

    def generate_data_insights(self, df, use_rag=True):
        """Generate insights for each column in the DataFrame."""
        insights = {}
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

                if use_rag:
                    try:
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=self.llm,
                            chain_type="map_reduce",
                            retriever=self.retriever,
                            return_source_documents=True
                        )
                        result = qa_chain({"query": prompt_with_values})
                        insights[column] = result['result']
                    except Exception as e:
                        print(f"Failed to generate insights using retrieval for {column} due to an error: {e}")
                else:
                    try:
                        response = self.llm.ask(prompt_with_values, log_level="info")
                        insights[column] = response
                    except Exception as e:
                        print(f"Failed to generate insights directly for {column} due to an error: {e}")

        return insights
