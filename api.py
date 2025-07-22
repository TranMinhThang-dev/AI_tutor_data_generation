from typing import Union, Annotated
from fastapi import FastAPI, UploadFile
from main import MainDataGeneration

data_gen = MainDataGeneration()
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)