#!/bin/bash

# setup boto
mv .boto /home/circleci/.boto

## DEBUG
cat 2600.json

gsutil ls

gsutil cp ../build/2600.md s3://linksbucket/
