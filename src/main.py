from server.server import run_server
from config.config import Config
from db.connection import global_init
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-file", required=True)
    parser.add_argument("--upload-folder", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    config = Config(args.db_file, args.upload_folder)
    global_init(config.database_file)
    run_server(config=config)


if __name__ == "__main__":
    main()