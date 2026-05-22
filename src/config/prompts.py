from pydantic_settings import BaseSettings


class Config(BaseSettings):
    FIGURE_DESCRIPTION_SYSTEM_MESSAGE: str = "Describe precisely what is shown on the image. Extract any meaningful data that is presetned graphically. " \
    "The description will be inserted into text so don't use language that indicates interaction with user."


PromptsConfig = Config() 