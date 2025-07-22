import os 
import io
from typing import Union
from dotenv import load_dotenv
from PIL import Image
from tqdm import tqdm
from modules.exercise_extractor import ExerciseExtractor
from modules.step_by_step_solver_model import StepByStepSolver
from modules.utils import pdf_pages_to_images
from loguru import logger
load_dotenv()

class MainDataGeneration:
    def __init__(self, save_path: str = "output.json", require_step_by_step_solution: bool = False):
        openai_api_key = os.getenv("LITELLM_API_KEY")
        openai_api_url = os.getenv("LITELLM_API_URL")

        self.exercise_extractor = ExerciseExtractor(
            api_key=openai_api_key,
            llm_model="gpt-4o",
            provider="openai",
            llm_host=openai_api_url
        )
        self.save_path = save_path
        self.require_step_by_step_solution = require_step_by_step_solution
        if self.require_step_by_step_solution:
            self.step_by_step_solver = StepByStepSolver(
                api_key=openai_api_key,
                llm_model="gpt-4o",
                provider="openai",
                llm_host=openai_api_url
            )
        else:
            self.step_by_step_solver = None

    def process_image(self, input_image: Union[str, bytes]) -> None:
        """Run the exercise extraction process."""
        logger.info("Starting exercise extraction in image...")
        try: 
            if isinstance(input_image, str):
                # If input is a file path, convert to bytes
                input_image = Image.open(input_image)
                buffer = io.BytesIO()
                input_image.save(buffer, format="JPEG", quality=95)
                input_image = buffer.getvalue()

            # Extract exercise list exercise from the image
            exercise_list = self.exercise_extractor.process(input_image)
            
            if self.require_step_by_step_solution:
                logger.info("Starting give step by step solution for each exercise...")
                for exercise in exercise_list.exercise_list:
                    solution = self.step_by_step_solver.process(exercise.question)
                    exercise.answer = solution

            for exercise in exercise_list.exercise_list:
                with open(self.save_path, 'a', encoding='utf-8') as f:
                    f.write(f"{exercise.model_dump_json()},\n")

            logger.success("Extracted exercises successfully.")
        except Exception as e:
            logger.error(f"Error during exercise extraction: {e} in line {e.__traceback__.tb_lineno}, code: {e.__traceback__.tb_frame.f_code.co_name}")

    def process_pdf(self, pdf_path: str) -> None:
        """Process a PDF file and extract exercises from each page."""
        logger.info("Starting exercise extraction in PDF...")

        try:
            images = pdf_pages_to_images(pdf_path)
            for image in tqdm(images, desc="Processing PDF pages:"):
                self.process_image(image)
            logger.success("Extracted exercises successfully.")
        except Exception as e:
            logger.error(f"Error processing PDF: {e} in line {e.__traceback__.tb_lineno}, code: {e.__traceback__.tb_frame.f_code.co_name}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract exercises from images or PDFs.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input image or PDF file.")
    parser.add_argument("--output", type=str, default="output.json", help="Path to save the extracted exercises.")
    parser.add_argument("--step-by-step", action="store_true", help="Whether to require step by step solution for each exercise.")

    args = parser.parse_args()

    data_generator = MainDataGeneration(save_path=args.output, require_step_by_step_solution=args.step_by_step)

    if args.input.lower().endswith('.pdf'):
        data_generator.process_pdf(args.input)
        logger.info(f"Processed pdf: {args.input}")
    else:
        data_generator.process_image(args.input)
        logger.info(f"Processed image: {args.input}")

    logger.info(f"Output saved to: {args.output}")
        