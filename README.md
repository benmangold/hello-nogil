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