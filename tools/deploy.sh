#!/bin/bash

# setup boto
cp .boto ~/.boto

gsutil cp ../build/2600.md s3://linksbucket/
