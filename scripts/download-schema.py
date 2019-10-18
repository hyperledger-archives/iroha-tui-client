#!/usr/bin/env python3

from six.moves import urllib
from pathlib import Path
import os.path
from os import chdir

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directory = str(Path(root_directory) / Path("torinaku"))
chdir(directory)
print("Working directory set to {}".format(directory))

BASE_URL = (
    "https://raw.githubusercontent.com/hyperledger/iroha/master/shared_model/schema/"
)

FILES = [
    "block.proto",
    "commands.proto",
    "endpoint.proto",
    "primitive.proto",
    "proposal.proto",
    "qry_responses.proto",
    "queries.proto",
    "transaction.proto",
]

for file in FILES:
    print(file)
    data = urllib.request.urlopen(BASE_URL + file)
    print("\tdownloading")
    with open(os.path.join("schema", file), "wb") as out:
        out.write(data.read())
        out.flush()
    print("\tsaved")

print("Done.")
