from pydantic_settings import BaseSettings


class Config(BaseSettings):
    FIGURE_DESCRIPTION_SYSTEM_MESSAGE: str = "Describe precisely what is shown on the image. Extract any meaningful data that is presetned graphically. " \
    "The description will be inserted into text so don't use language that indicates interaction with user."
    AUTHOR_AND_CITATION_SYSTEM_MESSAGE: str = "Drop any latex format residuals. " \
    "Return a cleaned up list of authors in format: 'FullSurname FullName, FullSurname FullName . . .' and a citation that follows this format: 'Surname N., Surname N. ..., 'Title', ArXiv, Year'"
    SECTION_SYSTEM_MESSAGE: str = "Translate whole section to polish and drop any latex markers. If there is a table or other similar structure, summarize it and include in translation. Generate a summary of section that describes the contents and provides key information."

PromptsConfig = Config() 