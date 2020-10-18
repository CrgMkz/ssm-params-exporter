## Usage

### Exporting:

Provide the param store path you want to download params from. '/' will download all parameters.

Also provide the region you want the parameters pulled from.

```
python3 main.py download --path ['path'] --region ['aws region']
```

Example:

```
python3 main.py download --path '/' --region eu-west-1
```

### Importing:

Provide the filename created from the step above.

Provide the AWS region you are importing the params to.

```
python3 main.py upload --filename ['filename'] --region ['aws region']
```

Example:

```
python3 main.py upload --filename params_eu-west-1_141020_2314.txt --region eu-west-1
```