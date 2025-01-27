import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def news_extract(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
             ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the news article page of a website.
            your job is to extract the content of news article and return the summarizes lenghty news articles into concise,easy-to-read summaries,keypoint form.
            divede in catagories if possible.
            Only return valid JSON.
            ### VALID JSON ONLY(NO PREAMBLE):
            """
)

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res 

    def write_summaries(self,json_res):
        prompt_summaries = PromptTemplate.from_template(
        """

        ### NEWS ARTICLE CONTENT:
        {news_article_content}
        ### INSTRUCTION:
        your job is to summarize the lenghty content of  above dictionary and formate into easy-to-read summaries.
        Ensure that keypoint are clear,and the summary is written in  simple language for quick understanding.
        Please generate a plain text summary of the following news report. Do not use any markdown syntax or special characters (like asterisks or underscores) for formatting.
        ### SUMMARY (NO PREAMBLE):
        """
        )
        chain_summaries = prompt_summaries | self.llm
        res = chain_summaries.invoke({"news_article_content":dict(json_res)})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))