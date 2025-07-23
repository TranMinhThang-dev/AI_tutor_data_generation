from typing import List, Optional
from pydantic import BaseModel, Field

class Exercise(BaseModel):
    question: str = Field(
        description=(
            """The full text of an individual exercise or question. Typically begins with Vietnamese keywords such as 
            'Bài', 'Câu', etc."""
        )
    )
    answer: Optional[str] = Field(
        description=(
            """The correct answer or solution to the exercise. This field is optional because some exercises may not have answers yet """
        )
    )

class ExerciseList(BaseModel):
    exercise_list: List[Exercise] = Field(
        description=(
            """A structured list of exercises, where each item contains a question (and optionally an answer). """
        )
    )

class ExerciseTitle(BaseModel):
    exercise_title_index: str = Field(description='Exercise title index')
    bounding_box: List[int] = Field(description='Bounding box of the Exercise title in (x_min, y_min, x_max, y_max) format')

class ExerciseBoundingBoxList(BaseModel):
    exercise_title_list: List[ExerciseTitle] = Field(description="A list of objects. Each object represents an exercise with an exercise title index (e.g., 'Bài 1', 'Câu 2', 'Câu 6.1', etc.) and its bounding box in (x_min, y_min, x_max, y_max) format.")
