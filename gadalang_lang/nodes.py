import sys
import argparse
import asyncio
import json
import binaryiotools
import pygada_runtime
from pygada_runtime import BinaryStream


def _json(argv):
    """lang.json node.

    Read JSON:

    .. code-block:: python

        # Read json from stdin
        gada lang.json
        gada lang.json --input -
        # Read json from file
        gada lang.json --input data.json
        # Receive json from previous node
        gada lang.json --chain-input

    Write JSON:

    .. code-block:: python

        # Write json to stdout
        gada lang.json --input data.json
        gada lang.json --input data.json --output -
        # Write json to file
        gada lang.json --input data.json --output data2.json
        # Send json to next node
        gada lang.json --input data.json --chain-output

    Other:

    .. code-block:: python

        # Indentation
        gada lang.json --indent 4
        
    """
    def work(args):
        s = BinaryStream(sys.stdin, sys.stdout)

        if not args.input or args.input == '-':
            # Read data from stdin
            data = sys.stdin.read()
            data = data[data.index("{"):data.rindex("}")+1]
            data = json.loads(data)
        else:
            # Read data from file
            with open(args.input, "r") as f:
                data = json.loads(f.read())

        if args.chain_output:
            # Pass to other nodes
            s.write_json(data)
        elif args.output and args.output != '-':
            # Write to file
            with open(args.output, "w+") as f:
                f.write(json.dumps(data, indent=args.indent))
        else:
            # Write to stdout
            print(json.dumps(data, indent=args.indent))

    parser = pygada_runtime.get_parser()
    parser.add_argument("--input", type=str, help="input file or - for stdin")
    parser.add_argument("--output", type=str, help="output file or - for stdout")
    parser.add_argument("--indent", type=int, help="json indentation")
    pygada_runtime.main(work, parser, argv)
