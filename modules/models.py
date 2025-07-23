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
