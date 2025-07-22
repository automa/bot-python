from automa.bot import CodeFolder, TaskForCode


def update(folder: CodeFolder, task: TaskForCode):
    """
    Update code in the specified folder.
    """

    # If adding a new file, use the following:
    # folder.add("example.py")
