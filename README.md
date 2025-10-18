# hello-nogil

Playing around without the GIL in Python 3.14.0.

**WARNING: Experimental.  Not for serious use.**

## Using this repo

1.  Build base image.  See `py314_nogil_base_image`

2.  Build and run test app.  See `test_app`

3.  ???

## py314_nogil_base_image

Removing the Python GIL requires building Python from source with particular configuration.

This Dockerfile does just that, producing a base image to use in test applications.

```bash
# build 'py314_nogil:latest' docker image
./py314_nogil_base_image/build_base_image.sh
```

## test_app

The simplest possible demonstration of GIL being off.

```
./test_app/build_test_app.sh
```

You should get some output like:

```
Is GIL enabled? False
Execution time with multiple threads: 0.20 seconds
Execution time with sequential calls: 0.65 seconds

```

## test_webserver

Run a server which shows the difference between GIL and no GIL.


Run server in docker, with no GIL

```
./test_webserver/build_webserver.sh
```

Run server with your host's Python, almost guaranteed to be with GIL

```bash
python test_webserver/main.py

```

Run a simple benchmark against which ever server is running:

```bash
 ab -n 100 -c 10 http://127.0.0.1:8000/

```

## Benchmark Results

### No GIL

```
ab -n 100 -c 10 http://127.0.0.1:8000/
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        687 bytes

Concurrency Level:      10
Time taken for tests:   1.130 seconds
Complete requests:      100
Failed requests:        91
   (Connect: 0, Receive: 0, Length: 91, Exceptions: 0)
Total transferred:      78692 bytes
HTML transferred:       68792 bytes
Requests per second:    88.47 [#/sec] (mean)
Time per request:       113.028 [ms] (mean)
Time per request:       11.303 [ms] (mean, across all concurrent requests)
Transfer rate:          67.99 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    21   57 147.8     30    1072
Waiting:       21   57 147.8     30    1072
Total:         21   57 147.8     30    1072

Percentage of the requests served within a certain time (ms)
  50%     30
  66%     39
  75%     42
  80%     45
  90%     56
  95%     68
  98%   1072
  99%   1072
 100%   1072 (longest request)
```

### GIL

```
 ab -n 100 -c 10 http://127.0.0.1:8000/
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /
Document Length:        681 bytes

Concurrency Level:      10
Time taken for tests:   2.366 seconds
Complete requests:      100
Failed requests:        91
   (Connect: 0, Receive: 0, Length: 91, Exceptions: 0)
Total transferred:      78092 bytes
HTML transferred:       68192 bytes
Requests per second:    42.26 [#/sec] (mean)
Time per request:       236.649 [ms] (mean)
Time per request:       23.665 [ms] (mean, across all concurrent requests)
Transfer rate:          32.23 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   43  55.3     31     222
Processing:    41  176  34.4    177     260
Waiting:       41  169  32.7    169     260
Total:         41  219  71.6    211     482

Percentage of the requests served within a certain time (ms)
  50%    211
  66%    237
  75%    255
  80%    272
  90%    301
  95%    361
  98%    397
  99%    482
 100%    482 (longest request)
 ```

