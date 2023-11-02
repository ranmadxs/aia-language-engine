from argparse import ONE_OR_MORE, ArgumentParser
from . import __version__
from .aia_languague_svc import startSvc

def run():
    """
    entry point
    """
    parser = ArgumentParser(prog="daemon", description="XD")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    #parser.add_argument(dest="users", nargs=ONE_OR_MORE, type="User", help="your name")
    #args = parser.parse_args()
    print ("start svc aia-ln-engine")
    startSvc()