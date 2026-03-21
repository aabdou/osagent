import csv
from tools import save_to_csv

def test_save_to_csv_success(tmp_path):
    mock_issues = [
        {"title": "Fix login bug", "url": "https://github.com/org/repo/issues/1"},
        {"title": "Add dark mode", "url": "https://github.com/org/repo/issues/2"},
        {"title": "Update docs", "url": "https://github.com/org/repo/issues/3"},
    ]

    result = save_to_csv(mock_issues, tmp_path)

    assert result.count == 3
    assert str(result.filepath).startswith(str(tmp_path))

    with open(result.filepath) as f:
        rows = list(csv.reader(f))

    assert len(rows) == 3
    assert rows[0] == ["Fix login bug", "https://github.com/org/repo/issues/1"]
    assert rows[1] == ["Add dark mode", "https://github.com/org/repo/issues/2"]
    assert rows[2] == ["Update docs", "https://github.com/org/repo/issues/3"]