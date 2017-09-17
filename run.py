import posts
import logging
import logging.config
import yaml

logger = logging.getLogger(__name__)

def main():
    logging.config.dictConfig(yaml.load(open('logconf.yaml', 'r')))
    logger.info("Caling posts main function")
    posts.main()
    logger.info("Function finished. Exiting...")

if __name__ == '__main__':
    main()