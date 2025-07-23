from modules.base import BaseLLMModule
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from modules.prompt import READ_INPUT_IMAGE_WITH_BOUNDING_BOX
from modules.models import ExerciseBoundingBoxList
from loguru import logger

class CropExerciseModel(BaseLLMModule):
    
    @property
    def parser(self):
        """Returns the output parser for crop exercise model"""
        return OutputFixingParser.from_llm(self.llm, PydanticOutputParser(pydantic_object=ExerciseBoundingBoxList)) 

    @property
    def prompt_template(self) -> ChatPromptTemplate:
        """Returns the prompt template for crop exercise model."""
        msg_template = HumanMessagePromptTemplate.from_template(
            template=[
                {"type": "text", "text": READ_INPUT_IMAGE_WITH_BOUNDING_BOX},
                {"type": "image_url", "image_url": "{encoded_image_url}"},
            ]
        )
        return ChatPromptTemplate(messages=[msg_template])
    
    @property
    def chain(self):
        """Returns the LangChain chain for crop exercise model."""
        return self.prompt_template | self.llm 
    
    def process(self, image: bytes) -> PydanticOutputParser:
        """Returns a step by step solution."""
        try:
            encoded_image = self._process_image_input(image)
            llm_output = self.chain.invoke({"encoded_image_url": encoded_image,
                                            "format_instruction": self.parser.get_format_instructions()})
            print(llm_output.content)
            
            return self.parser.parse(llm_output.content)
        except Exception as e:
            logger.error(f"Error {e} in line {e.__traceback__.tb_lineno}, code: {e.__traceback__.tb_frame.f_code.co_name}")
