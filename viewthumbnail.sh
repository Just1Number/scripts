#!/bin/sh
google-chrome $(http $1 | grep og:image | sed 's/^.*content="//' | sed 's/">//')
