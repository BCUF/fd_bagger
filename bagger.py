###
# Copyright BCU Fribourg 2022
# Author: nstulz
###

import logging
import argparse
import sys
import datetime
from ui import App
from logic import run


logger = logging.getLogger(__name__)

def init_log():

    parser = datetime.datetime.now() 
    time = parser.strftime("%d-%m-%Y_%H%M%S")

    logging.basicConfig(
        filename=f'bag_{time}.log',
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def main():

    init_log()

    # if no args are set it will use GUI
    if len(sys.argv) == 1:

        app = App()
        app.mainloop()

    # if args are set it will use the args
    else:

        parser = argparse.ArgumentParser(description='This program allows you to bag some dirs')
        optional = parser._action_groups.pop()
        required = parser.add_argument_group('required arguments')

        required.add_argument('-i','--input', type=str,
            help='The input file path', required=True)
        required.add_argument('-o','--output', type=str,
            help='The output directory', required=True)
        required.add_argument('-c','--callnumber', type=str,
            help='The callnumber, example: ARCHNUMFR_1664', required=True)

        optional.add_argument('-f','--fond', type=str,
            help="The fund's name", required=False, default="")
        optional.add_argument('-s','--startingnumber', type=int,
            help='Set the starting number', default=1)
        optional.add_argument('-d','--metadata', type=str,
            help='Set a metadata csv or json file', default=None)
        optional.add_argument('-m','--mcp', type=str,
            help='Set a mcp file', default=None)
        optional.add_argument('-p','--process', type=int,
            help='Set the number of process', default=1)

        parser._action_groups.append(optional)

        args = parser.parse_args()
        run(args.input, args.output, args.callnumber, args.fond, args.startingnumber, args.metadata, args.mcp, args.process)

        logging.info("Terminated")
        print("Terminated")

if __name__ == "__main__":
    main()