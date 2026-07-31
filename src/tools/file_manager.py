from typing import BinaryIO

from pathlib import Path
import shutil 
import zipfile
import tempfile 
import tarfile

from src.config.db import DBConfig

from time import sleep

class FileManager:
    def check_paper_exist(self, arxiv_signature: str, year: int) -> bool:
        storage_path = Path(DBConfig.LOCAL_STORAGE_PATH) / f"{arxiv_signature}_{year}"
        return storage_path.exists()

    async def process_directory(self, file: BinaryIO, arxiv_signature: str, year: int) -> list[tuple]:
        if self.check_paper_exist(arxiv_signature, year):
            raise 

        storage_path = Path(DBConfig.LOCAL_STORAGE_PATH) / f"{arxiv_signature}_{year}"
        storage_path.mkdir(parents=True, exist_ok=True)

        saved = []

        with tarfile.open(fileobj=file, mode="r:gz") as tar:
            for member in tar.getmembers():
                member_path = storage_path / member.name
                if member.isdir():
                    member_path.mkdir(parents=True, exist_ok=True)
                    saved.append(("dir", member.name))
                elif member.name.endswith((".tex", ".png", ".jpg", ".pdf")):
                    member_path.parent.mkdir(parents=True, exist_ok=True)
                    tar.extract(member, storage_path) 
                    saved.append(("file", member.name))
        
        return saved
