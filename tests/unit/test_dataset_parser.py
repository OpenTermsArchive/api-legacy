from datetime import datetime
from pathlib import Path
import sys
sys.path.append("./app/")

import pytest

from app.dataset_parser import CGUsDataset, CGUsFirstOccurenceParser

# test CGUsDataset
def test_path_check_ok():
    cgudataset = CGUsDataset(root_path="tests/test_dataset/")
    assert cgudataset

def test_path_check_not_a_directory():
    with pytest.raises(AssertionError, match = "is not a directory"):
        cgudataset = CGUsDataset(root_path="tests/test_dataset/FakeService/Community Guidelines/2020-11-09--17-30-22.md")

def test_path_check_directory_doesnt_exist():
    with pytest.raises(AssertionError, match = "does not exist"):
        cgudataset = CGUsDataset(root_path="tests/wrong_dir/")

def test_list_files():
    cgudataset = CGUsDataset(root_path="tests/test_dataset/")
    assert len(list(cgudataset.yield_all_md())) == 2
    assert len(list(cgudataset.yield_all_md(ignore_rootdir=False))) == 3

# test CGUsFirstOccurenceParser
def test_run_california():
    parser = CGUsFirstOccurenceParser(Path("tests/test_dataset"), "California")
    parser.run()
    output = parser.to_dict()
    assert set(output.keys()) == {"FakeService"}
    assert set(output["FakeService"].keys()) == {"Community Guidelines"}
    assert output["FakeService"]["Community Guidelines"] == datetime(2020, 11, 9, 17, 30, 22)

def test_run_rgpd():
    parser = CGUsFirstOccurenceParser(Path("tests/test_dataset"), "rgpd")
    parser.run()
    output = parser.to_dict()
    assert output["FakeService"]["Community Guidelines"] == datetime(2020, 11, 11, 16, 30, 22)

def test_run_not_found():
    parser = CGUsFirstOccurenceParser(Path("tests/test_dataset"), "Ambanum")
    parser.run()
    output = parser.to_dict()
    assert output["FakeService"]["Community Guidelines"] == False