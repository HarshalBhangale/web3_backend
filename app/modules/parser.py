from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import os
import json

load_dotenv()

from app.config import CurrencyConvertModel

OPENAI_KEY=os.environ['OPENAI_API_KEY']

class CurrencyParser():

    def __init__(self):
        model_name = 'text-davinci-003'
        temperature = 0.0
        self.model = OpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=OPENAI_KEY
        )

        self.parser = PydanticOutputParser(pydantic_object=CurrencyConvertModel)

        self.prompt = PromptTemplate(
            template="Get the amount to be converted\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def get_parsed_currency_convert(self, query: str):
        _input = self.prompt.format_prompt(query=query)
        output = self.model(_input.to_string())
        model = self.parser.parse(output).json()
        return json.loads(model)