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

import logging
import bagit
import argparse
import os
import shutil
import json
import csv
import pathlib
import shutil
from pathlib import Path
import datetime



logger = logging.getLogger(__name__)

bag_info = {
    "Source-Organization": "Bibliothèque_Universitaire_Cantonale_de_Fribourg"
}

def init_log(name):

    parser = datetime.datetime.now() 
    time = parser.strftime("%d-%m-%Y_%H%M%S")

    logging.basicConfig(
        filename=f'{name}_bag_{time}.log',
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def do_mapping(input_dir, output_dir, callnumber, fond, starting_number):

    mapping = []
    mapping_file_name = f"{callnumber}_mapping_lock.json"

    if os.path.isfile(f"{os.getcwd()}{os.path.sep}{mapping_file_name}"):

        logger.info(f"loading {mapping_file_name}")
        print(f"Loading {mapping_file_name}, erase this file if you want to restart completely")

        with open(mapping_file_name, encoding='utf8') as f:
            mapping = json.load(f)
            f.close()
        

    else:

        logger.info("create mapping...")

        files_without_parent_tmp_dir = ""

        # 1st copy the files without parent dir into files_without_parent_tmp_dir
        for name in sorted(os.listdir(input_dir)):

            try:

                current_path = f"{input_dir}{os.path.sep}{name}"
                

                if(os.path.isfile(current_path)):
                    
                    files_without_parent_tmp_dir = f"{os.getcwd()}{os.path.sep}fileWithoutParent_{callnumber}"

                    pathlib.Path(files_without_parent_tmp_dir).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(current_path, files_without_parent_tmp_dir)
            except Exception as e:
                logger.error('Something went wrong copying ' + name + ': '+ str(e))


        counter = starting_number

        for name in sorted(os.listdir(input_dir)):

            current_dir = f"{input_dir}{os.path.sep}{name}"

            if os.path.isdir(current_dir):

                logger.info(f"mapping: {current_dir}")

                fd = ""
                if len(fond) > 0:
                    fd = f"{fond.upper()}-"

                new_dir_name = f"{fd}{callnumber.upper()}-{'{:04}'.format(counter)}"

                new_dir = f"{output_dir}{os.path.sep}{new_dir_name}"
                dc_id = f"{callnumber.upper()}-{'{:04}'.format(counter)}"

                map_object = {}
                map_object["input"] = current_dir
                map_object["output"] = new_dir
                map_object["status"] = "INIT"
                map_object["dir_name"] = new_dir_name
                map_object["dc_id"] = dc_id.replace("_", " ")
                mapping.append(map_object)
                
                counter += 1

                
        if files_without_parent_tmp_dir != "":
            fd = ""
            if len(fond) > 0:
                fd = f"{fond.upper()}_"
            new_dir_name = f"{fd}{callnumber.upper()}-{'{:04}'.format(counter)}"
            new_dir = f"{output_dir}{os.path.sep}{new_dir_name}"
            map_object = {}
            map_object["input"] = files_without_parent_tmp_dir
            map_object["output"] = new_dir
            map_object["status"] = "INIT"
            map_object["dir_name"] = new_dir_name
            mapping.append(map_object)

    return mapping

def bag(mapping, input_dir, output_dir, callnumber, fond, metadata, mcp, process):

    logger.info(f"Start bagging with params: {input_dir}, {output_dir}, {callnumber}, {fond}, {metadata}, {mcp}, {process}")

    for m in mapping:

        try:

            if m["status"] != "SUCCESS":

                if os.path.exists(m["output"]):
                    shutil.rmtree(m["output"])
                    logger.info("deleted: " + m["output"])

                current_dir = m["input"]

                logger.info(f"Processing: {current_dir}")
                print(f"Processing: {current_dir}")

                name =  os.path.basename(os.path.normpath(m["input"]))

                new_dir_name = os.path.basename(os.path.normpath(m["output"]))

                data_dir = f'{m["output"]}{os.path.sep}skip-transfer-directory{os.path.sep}{name}'

                shutil.copytree(current_dir, data_dir)

                logger.info(f"Copying: {current_dir} in {data_dir}")

                bagit.make_bag(m["output"], bag_info=bag_info,  checksums=["md5"], processes=process)

                if metadata:

                    metadata_dir = f'{m["output"]}{os.path.sep}metadata'
                    os.makedirs(metadata_dir)
                    metadata_file = f"{metadata_dir}{os.path.sep}{os.path.basename(metadata)}"
                    shutil.copy2(metadata, metadata_file)

                    file_name, file_extension = os.path.splitext(metadata)

                    if file_extension == ".json":

                        with open(metadata_file, "r+", encoding='utf-8') as f:
                            data = json.load(f)

                            data[0]["filename"] = f"data/{new_dir_name}"

                            data[0]["dc.title"] = m["dir_name"]
                            data[0]["dc.identifier"] = m["dc_id"]

                            f.seek(0)       
                            json.dump(data, f, indent=4, ensure_ascii=False)
                            f.truncate()
                            f.close()
                    
                    elif file_extension == ".csv":

                        with open(metadata_file, 'r+', newline='', encoding='utf-8') as csvFile:

                            reader = csv.DictReader(csvFile, quoting=csv.QUOTE_MINIMAL)
                            dictobj = next(reader)
                        
                         
                            dictobj.update({'dc.title': m["dir_name"]})

                            dictobj.update({'dc.identifier': m["dc_id"]})

                            csvFile.seek(0)       
                            writer = csv.DictWriter(csvFile, quoting=csv.QUOTE_MINIMAL, fieldnames=list(dictobj.keys()))
                            writer.writeheader()
                            writer.writerow(dictobj)
                            csvFile.truncate()
                            csvFile.close()

                    else:
                        logger.info(f"file_extension not equals to .json or csv")


                if mcp:
                    new_dir = f"{output_dir}{os.path.sep}{new_dir_name}"
                    mcp_dir = f"{new_dir}{os.path.sep}{os.path.basename(mcp)}"
                    shutil.copy2(mcp, mcp_dir)

                m["status"] = "SUCCESS"
        
        except Exception as e:
            logger.error('Failed to handle ' + name + ': '+ str(e))
            m["status"] = "ERROR"
            continue

    mapping_file_name = f"{callnumber}_mapping_lock.json"

    without_parent_dir = f"{os.getcwd()}{os.path.sep}fileWithoutParent_{callnumber}"
    if os.path.exists(without_parent_dir):
        shutil.rmtree(without_parent_dir)
        logger.info("deleted: " + without_parent_dir)

    with open(f"{os.getcwd()}{os.path.sep}{mapping_file_name}", 'w', encoding='utf8') as json_file:
        json.dump(mapping, json_file, indent=4)
        #   rename folder with status error
        for folder in mapping:
            if folder["status"] == "ERROR":
                os.rename(folder["output"], f'{folder["output"]}_ERROR_DETECTED')

        

def main():

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

    init_log(args.callnumber)

    mapping = do_mapping(args.input, args.output, args.callnumber, args.fond, args.startingnumber)

    bag(mapping, args.input, args.output, args.callnumber, args.fond, args.metadata, args.mcp, args.process)

    logging.info("Terminated")
    print("Terminated")

if __name__ == "__main__":
    main()