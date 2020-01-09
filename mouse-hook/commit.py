
from datetime import datetime

class Commit:
    def __init__(self, commit, timestamp, message, insertions, deletions):
        self.commit = commit
        self.timestamp = timestamp
        self.message = message
        self.insertions = insertions
        self.deletions = deletions
        self.changes = insertions + deletions
    
    def __str__(self):
        return '{0}\t{1}\t{2}\t+{3}/-{4}'.format(
            self.commit,
            self.timestamp,
            self.message,
            self.insertions,
            self.deletions
        )


'''
arg log_output: result of call to
    git log --author="author" --format="commit %H %at %s" --numstat

commit ee57f69f622c0ade639b8748f3bc4d169e8343c 1578516928 test

2       0       mouse-hook/commit.py
16      0       mouse-hook/logic.py
1       0       test
commit dfe0df38bb16479a13976674f05f3ca4a5e6d1ee 1578514210 test

1       0       test
commit 1611f9efe69e46450890f1ca2ca2559cb9d4c735 1578513385 .gitignore

1       0       .gitignore
'''
def parse_commits(log_output):
    commits = []
    lines = log_output.decode('utf-8').splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('"commit'):
            commit_line = line.split()
            commit = commit_line[1]
            timestamp = datetime.fromtimestamp(int(commit_line[2]))
            message = ' '.join(commit_line[3:]).strip('"')
            # The next line is always empty
            index += 2
            line = lines[index]
            insertions = 0
            deletions = 0
            while not line.startswith('"commit'):
                i, d, _ = line.split('\t')
                insertions += int(i)
                deletions += int(d)
                index += 1
                if index == len(lines):
                    break
                line = lines[index]
            commits.append(Commit(commit, timestamp, message, insertions, deletions))
    return commits
