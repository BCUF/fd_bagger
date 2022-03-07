 # 
 # This file is part of the fd_bagger distribution (https://github.com/BCUF/fd_bagger).
 # Copyright (c) 2022 BCU Fribourg.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import argparse
import bagit
import datetime
import logging
import os.path
import shutil
import sys

logger = logging.getLogger(__name__)

def init_log():

    parser = datetime.datetime.now() 
    time = parser.strftime("%d-%m-%Y_%H%M%S")

    logging.basicConfig(
        stream = sys.stdout,
        level=logging.WARNING, 
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def main():

    parser = argparse.ArgumentParser(description='This program allows you to update an existing bag')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    required.add_argument('elements', metavar='elements', type=str, nargs='+',
                          help='path to directories or files to add')

    required.add_argument('-b','--bag', type=str,
        help='The bag to update', required=True)


    required.add_argument('-t','--target', type=str,
        help='Absolute path to the destination of the added elements within the bag', required=True)   


    parser._action_groups.append(optional)

    args = parser.parse_args()

    init_log()

    # first open the bag
    bag = bagit.Bag(args.bag)

    # now copy every elements
    for obj in args.elements:

        if os.path.exists(obj):
            if os.path.isfile(obj):
                shutil.copy2(obj, args.target + os.path.sep + os.path.basename(obj))
            elif os.path.isdir(obj):
                shutil.copytree(obj, args.target + os.path.sep + os.path.basename(obj))
        else:
            logging.error("File or directory does not exist: " + obj)

    # persist changes
    bag.save(manifests=True)

if __name__ == "__main__":
    main()
