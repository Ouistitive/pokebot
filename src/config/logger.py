

import logging


def set_logging(args):
    logging.basicConfig(
        filename="out.txt",
        filemode="w",
        level=logging.WARNING,
        format="%(name)s %(message)s",
    )
    
    logging.getLogger("players.heuristic").setLevel(
        logging.DEBUG if args.verbose else logging.WARNING
    )