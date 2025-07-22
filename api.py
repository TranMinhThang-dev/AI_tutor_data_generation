import tempfile
from typing import Union, Annotated
from fastapi import FastAPI, UploadFile
from main import MainDataGeneration

data_gen = MainDataGeneration(require_step_by_step_solution=True)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exercise Extractor API"}

@app.post("/extract_exercises/")
async def extract_exercises(image: UploadFile) -> None:
    try:
        content = await image.read()
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(content))
        image.save("img/temp_image.png")
        data_gen.process_image(content)
        return {"message": "Exercise extraction completed successfully!!!"}
    except Exception as e:
        return {"message": str(e)}


@app.post("/extract_exercises_pdf/")
async def extract_exercises_pdf(file: UploadFile, start_page: int = 0, end_page: int = -1) -> None:
    try:
        content = await file.read()
        with tempfile.TemporaryFile(suffix=".pdf", mode='wb', delete=True) as tmp_file:
            tmp_file.write(content)
            tmp_file.flush()
            pdf_path = tmp_file.name

        data_gen.process_pdf(pdf_path=pdf_path, start_page=start_page, end_page=end_page)
        return {"message": "Exercise extraction completed successfully!!!"}
    except Exception as e:
        return {"message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)