# XJson:
XJson is a shell executable Python tool which consumes a variable length sequence of JSON values from STDIN. The program then outputs 2 Json values. The first value is a Json Object with 2 fields, count, which contains the number of values read, and seq, which contains all values organized in order. The second value is a Json list, in which the first element is the number of values read, and the remaining elements contain the read Json values in reverse order.

### Prerequisites

* Python 3 - Double check that your python executable or symlink exists at /usr/bin/python3. If it doesn't, you will need to update the first line in xyes with the path to your python installation.

### Usage
Parse json from file

```cat <file> | ./xjson```  

Pass in json string directly

```echo <string> | ./xjson```
or
```./xjson``` and manually provide the input. Press Ctrl+D to end user input stream.

### Testing
Run the bash script `test_output.sh`

## Authors

* **Michael Tang
* **Nicholas Ding
