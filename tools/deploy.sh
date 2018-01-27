#!/bin/bash

# setup boto
mv .boto ~/.boto

## DEBUG
cat ~/2600.json

gsutil cp ../build/2600.md s3://linksbucket/
