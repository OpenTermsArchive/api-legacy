from abc import ABC, abstractmethod
from collections import Counter, defaultdict
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
        
    def list_all_services_doc_types(self, multiple_versions_only : bool = False) -> list:
        """
        Returns all services and document types in a dataset.
        """
        all_service_doctypes = Counter([(f.parts[-3], f.parts[-2]) for f in self.root_path.glob("**/*.md")])

        threshold = 1 if multiple_versions_only else 0

        all_filtered_service_doctypes = ((key[0], key[1]) for key, count in all_service_doctypes.items() if count > threshold)

        dict_out = defaultdict(list)
        for service, doc_type in all_filtered_service_doctypes:
            dict_out[service].append(doc_type)
        return dict(dict_out)


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
        version_date = datetime.strptime(
            file_path.name.rstrip(".md"), DATASET_DATE_FORMAT)
        service, document_type = file_path.as_posix().split("/")[-3:-1]
        return service, document_type, version_date

    def _file_contains(self, file_path: Path):
        with open(file_path, "r") as f:
            for line in f:
                if self.regex_term.search(line):
                    return True
        return False

    @staticmethod
    def _to_regex(comma_separated_terms: str):
        """
            Given a string of comma-separated terms,
            returns a Regex matching any of these terms.
            "hello,world,California Act" --> "hello|world|California Act"
        """
        return comma_separated_terms.replace(",", "|")


class CGUsFirstOccurenceParser(CGUsParser):

    def __init__(self, path, terms):
        super().__init__(path)
        self.regex_term = re.compile(
            rf"{self._to_regex(terms)}", re.IGNORECASE)

    def run(self):
        """
            For each service provider, and for each document type,
            return date of first occurence of a given term (or comma-separated terms), or `False`
        """
        self.output = dict()

        for md in self.dataset.yield_all_md(ignore_rootdir=True):
            service, document_type, version_date = self._parse_name(md)

            # TODO: clean and optimize this
            if service not in self.output.keys():
                self.output[service] = {document_type: False}

            if document_type not in self.output[service].keys():
                self.output[service] = {
                    **self.output[service], **{document_type: False}}

            if self._file_contains(md):
                if not self.output[service][document_type]:
                    self.output[service][document_type] = version_date
                elif version_date < self.output[service][document_type]:
                    self.output[service][document_type] = version_date

    def to_dict(self):
        return self.output

class CGUsAllOccurencesParser(CGUsParser):

    def __init__(self, path, terms):
        super().__init__(path)
        self.regex_term = re.compile(
            rf"{self._to_regex(terms)}", re.IGNORECASE)

    def run(self):
        """
            For each service provider, and for each document type,
            return date of first occurence of a given term (or comma-separated terms), or `False`
        """
        self.output = dict()

        for md in self.dataset.yield_all_md(ignore_rootdir=True):
            service, document_type, version_date = self._parse_name(md)


            # TODO: clean and optimize this
            if service not in self.output.keys():
                self.output[service] = {
                    document_type: {
                        version_date: False
                    }
                }

            if document_type not in self.output[service].keys():
                self.output[service] = {
                    **self.output[service], **{document_type: {version_date: False}}
                }

            self.output[service][document_type][version_date] = self._file_contains(md)

    def to_dict(self):
        return self.output
