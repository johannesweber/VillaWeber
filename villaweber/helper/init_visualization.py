from log import Logger
from visualisation import Visualisation

def main():
    logger = Logger().get_logger(logger_name='villaweber')
    visu = Visualisation(logger=logger)
    visu.init_configuration()

if __name__ == '__main__':
    main()