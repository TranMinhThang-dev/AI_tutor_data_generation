from typing import Union
from .base import BaseLLMModule
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from .models import ExerciseList
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from .prompt import EXERCISE_LIST_PARSER_PROMPT

class ExerciseExtractor(BaseLLMModule):
    
    @property
    def parser(self) -> PydanticOutputParser:
        """Returns the output parser for exercise list extraction."""
        return OutputFixingParser.from_llm(self.llm, PydanticOutputParser(pydantic_object=ExerciseList)) 

    @property
    def prompt_template(self) -> ChatPromptTemplate:
        """Returns the prompt template for exercise list extraction."""
        msg_template = HumanMessagePromptTemplate.from_template(
            template=[
                {"type": "text", "text": EXERCISE_LIST_PARSER_PROMPT},
                {"type": "image_url", "image_url": "{encoded_image_url}"},
            ]
        )
        return ChatPromptTemplate(messages=[msg_template])
    
    @property
    def chain(self):
        """Returns the LangChain chain for exercise list extraction."""
        return self.prompt_template | self.llm 
    
    def process(self, image: bytes) -> ExerciseList:
        """Extracts a list of exercise titles from an image."""
        try:
            encoded_image = self._process_image_input(image)
            # print(self.prompt_template.invoke({"encoded_image_url": encoded_image, 
            #                                    "schema": self.parser.get_format_instructions()}))
            llm_output = self.chain.invoke({"encoded_image_url": encoded_image, 
                                    "schema": self.parser.get_format_instructions()})
            llm_output = llm_output.content.strip().replace("```","").replace("json","")

            return self.parser.parse(llm_output)
        except Exception as e:
            from loguru import logger
            logger.error(f"Error {e} in line {e.__traceback__.tb_lineno}, code: {e.__traceback__.tb_frame.f_code.co_name}")
