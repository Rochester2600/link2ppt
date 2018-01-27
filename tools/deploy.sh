#!/bin/bash

# setup boto
mv .boto /home/circleci/.boto

## DEBUG
#cat 2600.json

#gsutil ls

gsutil cp -p ../build/* gs://linksbucket/
