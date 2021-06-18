import os
import sys
import argparse
import subprocess
import yaml
from pathlib import Path
from typing import List

DESC = '''test the output of the e3sm_to_cmip package from 
two git branches and run a comparison check on the output. Returns 0 if 
all checks run successfully, 1 otherwise. These checks
use the included CWL workflows to post-process the data and prepare it 
to  be ingested by e3sm_to_cmip.

At the moment it only tests atmospheric monthly variables, but more will be added in the future'''


def test(vars: List, branch: str, input: Path, output: Path):
    if not input.exists():
        raise ValueError(f"Input directory {input} does not exist")
    output.touch(exist_ok=True)

    cmd = 'git status'
    p = subprocess.check_call(cmd)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog='e3sm_to_cmip',
        description=DESC)
    parser.add_argument(
        'input', 
        help='directory of raw files to use, these should be native grid raw model output')
    parser.add_argument(
        '--output', 
        default='testing', 
        help=f'path to where the output files from the test should be stored, default is {os.environ.get("PWD")}{os.sep}testing{os.sep}')
    parser.add_argument(
        '--cleanup', 
        action='store_true', 
        help='remove the generated data if the test result is a success')
    parser.add_argument(
        '-v', '--var-list', 
        default='all', 
        nargs="*",
        help='select which variables to include in the comparison, default is all')
    parser.add_argument(
        '-c', '--compare', 
        default='master', 
        help='select which branch to run the comparison against, default is master')
    parsed_args = parser.parse_args()

    try:
        retval = test(
            vars=parsed_args.var_list, 
            branch=parsed_args.compare, 
            input=Path(parsed_args.input))
    except Exception as e:
        print(e)
        retval = 1
    # if the test returns a 0, then it was successful
    if retval == 0 and parsed_args.cleanup:
        os.rmdir(parsed_args.output)
    return retval

if __name__ == "__main__":
    sys.exit(main())