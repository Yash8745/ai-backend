import os
import time
import sys
from langchain.callbacks.base import BaseCallbackHandler # type: ignore

PINECONE_API_KEY = "077cedce-098f-420e-a7bc-3abe324476b5"
os.environ["GROQ_API_KEY"] = "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"

class TypewriterCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        sys.stdout.write(token)
        sys.stdout.flush()
        time.sleep(0.02)
