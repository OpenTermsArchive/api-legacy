from datetime import datetime
from pathlib import Path

from config import CGUS_DATASET_PATH, DATASET_DATE_FORMAT


class CGUsDataFinder:  # pylint: disable=too-few-public-methods
    """
    Helper class to find a specific version in the dataset for a given service and doc_type
    """

    def __init__(self, service: str, doc_type: str):
        self.service = service
        self.doc_type = doc_type
        self.path = Path(CGUS_DATASET_PATH, self.service, self.doc_type)
        self.__validate_path(self.path)
        self.versions = {
            datetime.strptime(
                file_path.name.rstrip(".md"), DATASET_DATE_FORMAT
            ): file_path
            for file_path in self.path.glob("*.md")
        }

    def get_version_at_date(self, date: datetime):
        """
        Given a date, return information about the closest recorded version
        """
        versions_around_date = self._get_versions_around_date(date)
        date_before = versions_around_date.get("version_at_date", False)
        data = ""
        if date_before:
            data = self.versions[date_before].read_text()

        date_after = versions_around_date.get("next_version", False)

        return {
            "service": self.service,
            "doc_type": self.doc_type,
            "date": date.isoformat(),
            "version_at_date": date_before.isoformat() if date_before else False,
            "data": data,
            "next_version": date_after.isoformat() if date_after else False,
        }

    def _get_versions_around_date(self, date: datetime):
        """
        Given a date, returns the closest captured version before the date and after the date.
        """
        closest_anterior_version = None
        closest_posterior_version = None
        all_versions = self._list_ordered_version_dates()
        first_version = all_versions[0]

        if date < first_version:
            return {"version_at_date": None, "next_version": first_version}

        for i, version_date in enumerate(all_versions):
            if version_date < date:
                closest_anterior_version = all_versions[i]
                try:
                    closest_posterior_version = all_versions[i + 1]
                except IndexError:
                    closest_posterior_version = None
        return {
            "version_at_date": closest_anterior_version,
            "next_version": closest_posterior_version,
        }

    def _list_ordered_version_dates(self):
        ordered_version_dates = list(self.versions.keys())
        ordered_version_dates.sort()
        return ordered_version_dates

    @staticmethod
    def __validate_path(path: Path):
        if (
            not Path(CGUS_DATASET_PATH).resolve() in path.resolve().parents
            or not path.exists()
        ):
            raise Exception(f"Filename {path} is not in the dataset directory")
        return True


class NoVersionAtDateException(Exception):
    """
    Used when a user asks for a date before we started tracking the service
    """
