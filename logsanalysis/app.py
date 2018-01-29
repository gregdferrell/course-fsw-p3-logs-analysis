from logsanalysis.log_service import get_authors


if __name__ == "__main__":
    for author in get_authors():
        print(author)
