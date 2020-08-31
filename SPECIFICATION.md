# Specification

Implement a key-value server which is accessible from the network by a client.

## Required operations
The server should have the following operations:

- [ ] Storing a value: the client sends the key and the value for the server.
- [ ]  Retrieving a value: the client specifies the key, and the server must reply with the value associated to it.
    - [ ] If there's no value associated with the specified key, then the server should return a message indicating this.
- [ ]  Finding a value: the client specifies a prefix. The server returns all the keys whose value starts with
the prefix specified by the client.

- [ ] Key and value should be strings.

Any requirement not specified here is up to you.

## Details
- Code must be written in Python 3 and run on Linux.
- Write production-grade code, use consistent coding style. Code quality matters.
- Any open source library can be used which is available publicly. 3rd party libraries should be specified in requirements.txt file.
- Network should be IPv4, on top of this any protocol or message format is up to you
- Performance is not particularly important

## Required

- requirements.txt
- zip
