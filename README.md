# appconstructor

Documentation pending.

You can run the demo from the root directory with

```
python demo
```

The demo configuration can be found in `demo/app.sample.cfg`; it provides examples for defining resource dependencies, values and global values.

## Development Setup

To install for development, run

```
ENV=dev python setup.py develop
```

The `ENV=dev` variable will cause dev dependencies to be installed. Omitting it will install only dependencies required for production.

## Running linter

To check code style, run

```
./scripts/lint
```

## TODO

* Documentation
* Tests