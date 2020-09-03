## Remarks

- I would never implement a key-value server for any other purpose than a demonstration. It is not necessary reinvent the wheel and create an YAKVS (yet another key-value server)
- In production I would use memcache or Redis (if persistence is important).
- If searching keys by value was required and preformance was important I would use a document database such as MongoDB or CouchDB.

## Known limitations

- Probably can handle only one client-server connection in the same time.
- The logging is a bit underconfigured and verbose.
- The server should not run while functional tests are running

##  How to install or build the software?

> :warning: required python version `>= 3.7`
>
> `requirements.txt` is provided but it is not necessary

##  How to install or build the software
1. unzip `jakabk-key-value-server.zip` to `$HOME/key-value-server`
2. create a virtualenv and activate it (change your directory to `$HOME/key-value-server` if necessary)
   - I'm using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) for creating and managing virtualenvs
3. install with pip

```bash
unzip jakabk-key-value-server.zip $HOME/key-value-server
mkvirtualenv -a key-value-server -p python3.7
pip install .
```

## How to start the server?
1. activate the `key-value-server` virtualenv (change your directory to `$HOME/key-value-server` if necessary)
   - if you use `virtualenvwrapper` you can use `workon` command
2.  start-server default it will be listen on `<your-ip>:5555`

```bash
workon key-value-server
start-server
```

##  How can we try the server and see that it is working (feel free to create an example code, demo client, etc.)?
1. you can use `./demo-client`
2. for further cases please see: the tests/functional/test_server.py tests

## How to run the tests (if there are any)?
1. activatejj the `key-value-server` virtualenv (change your directory to `$HOME/key-value-server` if necessary)
2. install test requirements
3. run test with pytest

```
workon key-value-server
pip install .[test]
pytest tests --cov key_value_server
```

## For implementing TCP connection interface these resources were used
- https://pymotw.com/3/socket/tcp.html
- https://realpython.com/python-sockets/#echo-client-and-server
- https://stackoverflow.com/a/17668009/2553200
