from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path, PosixPath
import re
from config import DATASET_DATE_FORMAT

class CGUsDataset:
    """
    Helper class for handling CGUs Versions
    """

    def __init__(self, root_path: str = "../OpenTermsArchive-versions"):
        self.root_path = Path(root_path)
        assert self.root_path.exists(), f"{root_path} does not exist"
        assert self.root_path.is_dir(), f"{root_path} is not a directory"

    def yield_all_md(self, ignore_rootdir: bool = True) -> list:
        """
        Yield a list of all recorded versions (.md files) in the dataset
        Args:
            ignore_rootdir: used to ignore README.md when run against a repository
        """
        if ignore_rootdir:
            return self.root_path.glob("**/*/*.md")
        return self.root_path.glob("**/*.md")

    def list_all_services_doc_types(self, multiple_versions_only: bool = False) -> list:
        """
        Returns all services and document types in a dataset.
        """
        all_service_doctypes = Counter(
            # pylint: disable=line-too-long
            [(f.parts[-3], f.parts[-2]) for f in self.root_path.glob("**/*.md") if not f.match('README.md')]
        )

        threshold = 1 if multiple_versions_only else 0

        all_filtered_service_doctypes = (
            (key[0], key[1])
            for key, count in all_service_doctypes.items()
            if count > threshold
        )

        dict_out = defaultdict(list)
        for service, doc_type in all_filtered_service_doctypes:
            dict_out[service].append(doc_type)
        return dict(dict_out)

    def get_stats(self):
        """
        Extract basic info for every CGU in historical dataset
        """
        all_stats = dict()
        for file_path in self.yield_all_md(ignore_rootdir=True):
            cgu = CGU(file_path, is_historical=True)
            all_stats[cgu.fullname] = cgu.to_dict()
        return all_stats


class CGUsParser(ABC):
    """
    Abstract base class for parsing a CGU dataset
    """

    def __init__(self, path: PosixPath):
        self.path = path
        self.dataset = CGUsDataset(self.path)
        self.regex_term = None
        self.output = None

    @abstractmethod
    def run(self):
        """
        Run parser
        """

    @abstractmethod
    def to_dict(self):
        """
        Serialize parser in dict
        """

    @staticmethod
    def _parse_name(file_path):
        """
        Given a file path in the CGUs dataset,
        return the service, the document_type, and the version date
        """
        version_date = datetime.strptime(
            file_path.name.rstrip(".md"), DATASET_DATE_FORMAT
        )
        service, document_type = file_path.as_posix().split("/")[-3:-1]
        return service, document_type, version_date

    def _file_contains(self, file_path: Path):
        with open(file_path, "r") as file:
            for line in file:
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
    """
    Parser to find first occurence of a term in a dataset
    """

    def __init__(self, path, terms):
        super().__init__(path)
        self.regex_term = re.compile(rf"{self._to_regex(terms)}", re.IGNORECASE)

    def run(self):
        """
        For each service provider, and for each document type,
        return date of first occurence of a given term (or comma-separated terms), or `False`
        """
        self.output = dict()

        for markdown in self.dataset.yield_all_md(ignore_rootdir=True):
            service, document_type, version_date = self._parse_name(markdown)

            # TODO: clean and optimize this
            if service not in self.output.keys():
                self.output[service] = {document_type: False}

            if document_type not in self.output[service].keys():
                self.output[service] = {
                    **self.output[service],
                    **{document_type: False},
                }

            if self._file_contains(markdown):
                if not self.output[service][document_type]:
                    self.output[service][document_type] = version_date
                elif version_date < self.output[service][document_type]:
                    self.output[service][document_type] = version_date

    def to_dict(self):
        return self.output


class CGUsAllOccurencesParser(CGUsParser):
    """
    Parser to find all occurences of a term in a dataset
    """

    def __init__(self, path, terms):
        super().__init__(path)
        self.regex_term = re.compile(rf"{self._to_regex(terms)}", re.IGNORECASE)

    def run(self):
        """
        For each service provider, and for each document type,
        return date of first occurence of a given term (or comma-separated terms), or `False`
        """
        self.output = dict()

        for markdown in self.dataset.yield_all_md(ignore_rootdir=True):
            service, document_type, version_date = self._parse_name(markdown)

            # TODO: clean and optimize this
            if service not in self.output.keys():
                self.output[service] = {document_type: {version_date: False}}

            if document_type not in self.output[service].keys():
                self.output[service] = {
                    **self.output[service],
                    **{document_type: {version_date: False}},
                }

            self.output[service][document_type][version_date] = self._file_contains(
                markdown
            )

    def to_dict(self):
        return self.output


class CGU:  # pylint: disable=too-few-public-methods
    """
    A CGU object.
        The `is_historical` argument allows for parsing a historical CGUs-versions
        dataset which has a slightly different naming convention.
    """

    def __init__(self, path: PosixPath, is_historical: bool = False):
        self._path = path
        self.is_historical = is_historical
        # parse info from file path differently depending on the mode
        if self.is_historical:
            self.version_date = datetime.strptime(
                self._path.name.replace(".md", ""), DATASET_DATE_FORMAT
            )
            self.name = self._path.as_posix().split("/")[-2]
            self.service = self._path.as_posix().split("/")[-3]
            self.fullname = f"{self.service} - {self.name} - {self.version_date}"
        else:
            self.name = self._path.name.replace(".md", "")
            self.service = self._path.as_posix().split("/")[-2]
            self.fullname = f"{self.service} - {self.name}"
        self.document_type = f"{self.name}"

    def to_dict(self) -> dict:
        """
        "Serialize" the CGU object to key/value pairs.
        """
        output = {
            "service": self.service,
            "document_type": self.document_type,
        }
        if self.is_historical:
            output[
                "date"
            ] = self.version_date  # as string so that it can be serialized to json
        return output
