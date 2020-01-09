import pytest
from datetime import datetime
from logic import compute_historical_weight
from commit import Commit, parse_commits

def test_compute_weight():
    commits = [
        Commit(None, datetime(2020, 1, 1, 5), None, 5, 5),  # 30 + 0.5
        Commit(None, datetime(2020, 1, 1, 6), None, 2, 3),  # 30.5 + 0.25
        Commit(None, datetime(2020, 1, 1, 7), None, 3, 2),  # 30.75 + 0.25
        Commit(None, datetime(2020, 1, 3, 8), None, 20, 5)  # 31 + 1.25 - 1 = 31.25
    ]
    assert compute_historical_weight([commits[0]]) == 30.5
    assert compute_historical_weight([commits[0], commits[1]]) == 30.75
    assert compute_historical_weight([commits[0], commits[1], commits[2]]) == 31
    assert compute_historical_weight([commits[0], commits[1], commits[2], commits[3]]) == 31.25

@pytest.mark.skip
def test_parse_commits():
    s = '"commit 0ee57f69f622c0ade639b8748f3bc4d169e8343c 1578516928 test"\n\n2\t0\tmouse-hook/commit.py\n16\t0\tmouse-hook/logic.py\n1\t0\ttest\n"commit dfe0df38bb16479a13976674f05f3ca4a5e6d1ee 1578514210 test"\n\n1\t0\ttest\n"commit 1611f9efe69e46450890f1ca2ca2559cb9d4c735 1578513385 .gitignore"\n\n1\t0\t.gitignore\n"commit a08afad104a58c341c040a074b284d296510eed9 1578513292 test"\n\n0\t0\ttest\n"commit f8eaba88405389f80258be7ccdaa988ac3358caf 1578512238 Initial commit"\n\n1\t0\tREADME.md\n'
    
    commits = parse_commits(s)
    assert len(commits) == 5

    assert commits[0].commit == '0ee57f69f622c0ade639b8748f3bc4d169e8343c'
    assert commits[0].timestamp == '1578516928'
    assert commits[0].message == 'test'
    assert commits[0].insertions == 19
    assert commits[0].deletions == 0

    assert commits[1].commit == 'dfe0df38bb16479a13976674f05f3ca4a5e6d1ee'
    assert commits[1].timestamp == '1578514210'
    assert commits[1].message == 'test'
    assert commits[1].insertions == 1
    assert commits[1].deletions == 0

    assert commits[2].commit == '1611f9efe69e46450890f1ca2ca2559cb9d4c735'
    assert commits[2].timestamp == '1578513385'
    assert commits[2].message == '.gitignore'
    assert commits[2].insertions == 1
    assert commits[2].deletions == 0

    assert commits[3].commit == 'a08afad104a58c341c040a074b284d296510eed9'
    assert commits[3].timestamp == '1578513292'
    assert commits[3].message == 'test'
    assert commits[3].insertions == 0
    assert commits[3].deletions == 0

    assert commits[4].commit == 'f8eaba88405389f80258be7ccdaa988ac3358caf'
    assert commits[4].timestamp == '1578512238'
    assert commits[4].message == 'Initial commit'
    assert commits[4].insertions == 1
    assert commits[4].deletions == 0


    