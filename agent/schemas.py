from instructor import Instructor
from pydantic import BaseModel


class ClientBase(BaseModel):
    client: Instructor
    model: str

    model_config = {"arbitrary_types_allowed": True}
