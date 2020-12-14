#!/bin/bash
set -eu
PROJECT_PATH=$(dirname $(dirname "$(realpath -s "$0")"))
EXPECTED_OUTPUT_PATH="${PROJECT_PATH}/Test/1-out.json"
INPUT_PATH="${PROJECT_PATH}/Test/1-in.json"

EXPECTED_OUTPUT=$(cat $EXPECTED_OUTPUT_PATH)
ACTUAL_OUTPUT=$(cat $INPUT_PATH | "${PROJECT_PATH}/xjson")
echo "expected: ${EXPECTED_OUTPUT}"
echo "actual: ${ACTUAL_OUTPUT}"
if [ "$EXPECTED_OUTPUT" == "$ACTUAL_OUTPUT" ]; then
  echo "SUCCESS: Actual output is equal to expected output."
  exit 0
else
  echo "FAILURE: Actual output is not equal to expected output"
  exit 1
fi
