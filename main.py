from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
import config
import uvicorn
import logging

from helpers.function_helpers.file_handler import (
    FileTypeChecker,
    FileContentExtractor,
    ExtractorFactory,
    ConvertFileObject,
)
from helpers.function_helpers.text_processor import Chatbot

logger = logging.getLogger("MAIN")


# Create an instance of the FastAPI class
app = FastAPI(timezone=config.TIMEZONE)


# POST: Webhook
@app.post("/zania/chat")
async def zania_chat(
    questions: UploadFile = File(...), data: UploadFile = File(...)
):
    try:
        # Questions
        FileTypeChecker(allowed_types=["application/json"]).check(
            content_type=questions.content_type
        )

        # Data
        FileTypeChecker().check(content_type=data.content_type)

        # Raw Data
        raw_text = FileContentExtractor(
            ExtractorFactory()
        ).process_file(
            file_obj=data.file, content_type=data.content_type
        )

        # Question Object
        json_object = FileContentExtractor(
            ExtractorFactory(as_text=False)
        ).process_file(
            file_obj=questions.file, content_type=questions.content_type
        )

        if not (json_object and isinstance(json_object, list)):
            return JSONResponse(
                content={
                    "status": False,
                    "message": "Questions file is not proper",
                },
                status_code=400,
            )

        output = Chatbot(
            vector_db_type="redis", llm_model_type="openai"
        ).answer_questions(text_data=raw_text, questions=json_object)

        # Convert dictionary to JSON and store it in an in-memory file-like object
        file_obj = ConvertFileObject(output).to_json_file()

        # Return the in-memory file as a response
        return StreamingResponse(
            file_obj,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment;filename=answers.json"
            },
        )

    except Exception as e:
        logger.error("FUNCTION HELPER - ZANIA CHAT: {}".format(e))
        return JSONResponse(
            content={
                "status": False,
                "message": "Internal Server Error",
            },
            status_code=500,
        )


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
