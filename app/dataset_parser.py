from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from pathlib import Path, PosixPath
import re

from config import DATASET_DATE_FORMAT

class CGUsDataset():
    """
    Helper class for handling CGUs Versions
    """

    def __init__(self, root_path: str = "../CGUs-versions"):
        self.root_path = Path(root_path)
        assert self.root_path.exists(), f"{root_path} does not exist"
        assert self.root_path.is_dir(), f"{root_path} is not a directory"


    def yield_all_md(self, ignore_rootdir: bool = True) -> list:
        if ignore_rootdir:
            return self.root_path.glob('**/*/*.md')
        else:
            return self.root_path.glob('**/*.md')


class CGUsParser(ABC):
    """
        Abstract base class for parsing a CGU dataset
    """
    def __init__(self, path: PosixPath):
        self.path = path
        self.dataset = CGUsDataset(self.path)
    
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass
    
    @staticmethod
    def _parse_name(file_path):
        """
            Given a file path in the CGUs dataset,
            return the service, the document_type, and the version date
        """
        version_date = datetime.strptime(file_path.name.rstrip(".md"), DATASET_DATE_FORMAT)
        service, document_type = file_path.as_posix().split("/")[-3:-1]
        return service, document_type, version_date



class CGUsFirstOccurenceParser(CGUsParser):

    def __init__(self, path, term):
        super().__init__(path)
        self.regex_term = re.compile(rf"{term}")
    
    def run(self):
        """
            For each service provider, and for each document type,
            return date of first occurence of a given term, or `False`
        """
        self.output = defaultdict(lambda val: val)

        for md in self.dataset.yield_all_md(ignore_rootdir=True):
            service, document_type, version_date = self._parse_name(md)
            print(f"Handling {service} {document_type} {version_date}")
            
            # TODO: clean and optimize this
            if service not in self.output.keys():
                self.output[service] = {document_type: False}

            if document_type not in self.output[service].keys():
                self.output[service] = {**self.output[service], **{document_type: False}}

            if self._file_contains(md):
                if not self.output[service][document_type]:
                    self.output[service][document_type] = version_date
                elif version_date < self.output[service][document_type]:
                    self.output[service][document_type] = version_date


    def to_dict(self):
        return self.output

    def _file_contains(self, file_path: Path):
        with open(file_path, "r") as f:
            for line in f:
                if self.regex_term.search(line):
                    return True
        return False




