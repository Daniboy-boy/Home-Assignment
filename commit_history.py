import git
from git.objects.blob import Blob
from git.objects.commit import Commit
from typing import Dict, Any
from datetime import datetime, timezone
import os
import sys

def make_timezone_aware(dt):
    return dt.replace(tzinfo=timezone.utc)

def get_line_count_before_commit(commit: Commit, repo: git.Repo, file_path: str) -> int:
    # Get the file blob for the previous commit
    total_lines_before = 0
    previous_commit = commit.parents[0] if commit.parents else None
    try:
        if previous_commit:
            previous_blob = previous_commit.tree / file_path
            total_lines_before = len(previous_blob.data_stream.read().decode("utf-8").splitlines())
    except Exception as e:
        print(f"Error reading lines for {file_path}: {e}")

    return total_lines_before
def get_commit_info(commit: git.objects.commit.Commit, repo: git.Repo, total_stats: Dict[str, Any], commit_number: int) -> None:

    print(f"\n\033[1;34mCommit {commit_number}:\033[0m")
    print(f"\nMessage: {commit.message}")
    commit_id = commit.hexsha
    commit_parent_ids = [parent.hexsha for parent in commit.parents]
    print(f"Commit ID: {commit_id}")

    if commit_parent_ids:
        print(f"Parent IDs: {', '.join(commit_parent_ids)}")
    else:
        print("No parent IDs (initial commit or orphan branch).")

    print(f"Author: {commit.author.name} <{commit.author.email}>")
    print(f"Author Timestamp: {datetime.utcfromtimestamp(commit.authored_date).strftime('%Y-%m-%d %H:%M:%S')}")

    branches = [str(branch) for branch in repo.branches if commit in repo.iter_commits(branch)]
    print(f"Branches Pointing to the Commit: {', '.join(branches)}")

    tags = [tag.name for tag in repo.tags if commit in repo.iter_commits(tag)]
    print(f"Tags: {', '.join(tags)}" if tags else "No Tags")

    total_insertions = commit.stats.total['insertions']
    total_deletions = commit.stats.total['deletions']
    total_files_changed = commit.stats.total['files']

    print(f"Total Lines Added: {total_insertions}")
    print(f"Total Lines Removed: {total_deletions}")
    print(f"Total Files Changed: {total_files_changed}")

    total_stats['authors'].add(commit.author.email)
    total_stats['lines_added'] += total_insertions
    total_stats['lines_deleted'] += total_deletions
    total_stats['files_touched'].update(commit.stats.files)

    # Show files that were changed
    print("\nChanged files:")
    for file_path in commit.stats.files:
        lines_before_commit = get_line_count_before_commit(commit, repo, file_path)
        lines_after_commit = len(repo.git.show(f"{commit.hexsha}:{file_path}").splitlines())

        # Calculate percentage of lines added or deleted per file
        percentage_lines_added = ((lines_after_commit - lines_before_commit) / lines_before_commit) * 100 if lines_before_commit > 0 else 0
        print(f"\nFile: {file_path}")
        print(f"Lines Before Commit: {lines_before_commit}")
        print(f"Lines After Commit: {lines_after_commit}")
        print(f"Percentage Change in Lines of Code: {percentage_lines_added:.2f}%")

def main(repo_path: str, branch_name: str = "main") -> None:
    # Note: No need to clone the repository, as established in the task instructions.
    # The script assumes that the local .git file is available on the machine where it's executed.
    repo = git.Repo(repo_path)
    repo_name = os.path.basename(repo_path)
    # Get the specified branch or use the default branch if not provided
    branch = repo.branches[branch_name]

    commits = list(repo.iter_commits(branch, max_count=5))

    # Initialize variables for summary information
    total_stats = {
        'authors': set(),
        'lines_added': 0,
        'lines_deleted': 0,
        'files_touched': set()
    }

    # Print information about the commits
    print(f"Last 5 commits for repository '{repo_name}', branch '{branch_name}':")
    for i, commit in enumerate(commits):
        get_commit_info(commit, repo, total_stats,i)

    first_commit_date = make_timezone_aware(min(commit.authored_datetime for commit in commits))
    last_commit_date = make_timezone_aware(max(commit.authored_datetime for commit in commits))
    current_date = make_timezone_aware(datetime.utcnow())

    time_passed_since_first_commit = current_date - first_commit_date
    time_passed_since_last_commit = current_date - last_commit_date

    # Print summary information
    print("\n\033[1;34mSummary Information:\033[0m")
    print(f"Total unique authors: {len(total_stats['authors'])}")
    print(f"Total lines added: {total_stats['lines_added']}")
    print(f"Total lines deleted: {total_stats['lines_deleted']}")
    print(f"Total files touched: {len(total_stats['files_touched'])}")
    print(f"Time passed since first commit: {time_passed_since_first_commit}")
    print(f"Time passed since last commit: {time_passed_since_last_commit}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python my_script.py /path/to/repo [branch_name]")
    else:
        repo_path = sys.argv[1]
        branch_name = sys.argv[2] if len(sys.argv) == 3 else "main"
        main(repo_path, branch_name)
