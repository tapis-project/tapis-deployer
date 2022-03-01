# Tapis Deployer 

This tool generates the scripts and Kubernetes YAML used to stand up an instance of Tapis.

## Usage

Tapis Deployer works in two phases:

File Generation:

    1. Generate a complete input.yml file from either an interactive prompt, a start file (also in yml), or a combination of the two.
    2. Feed the complete input.yml generated in Step 1 to the kube generator to generate a directory of Kubernetes yaml files.

Deployment:

    3. Deploy the Tapis software to Kubernetes using the directory of Kubernetes files generates in Step 2 of File Generation.

## Run input-generator

The input generate accomplishes step 1 of file generation. The program source code is contained within the `inputgen` directory. The program
is also packaged as a Docker image, `tapis/deployer-input-gen`. 

To run with the Docker image, run a command in the following format:

```
   $ docker run --rm -v /path/on/host:/data -it tapis/deployer-input-gen <options>
```

For example,

```
  $  docker run --rm -v $(pwd)/output:/data -it tapis/deployer-input-gen --out=/data --start=/data/start_file.yml
```

The above command will mount a directory called "output" in the current workding directory into the deployer-input-gen container so that
the outputs written to `/data` in the container can be retained after the container is removed. Additionally, the command above specifes some flags to the input generator program, specifically, the `--out=/data --start=/data/start_file.yml`. 

You can see full documentation on how to run input generator via the help flag:

```
  $ docker run --rm -v $(pwd)/output:/data -it tapis/deployer-input-gen -h
```

The input generator program will prompt you for the values for different inputs. You can use a start file (the `--start` flag) to have input
generator retrieve the values from a yaml file and not prompt you.

You can quit the program at any time by entering `_QUIT` at a prompt. Input generator will save your work to a file (called `start_file.yml`)
which can then be used to resume from where you left off.


## Run Deployer Diagnostics
If you want to look for internal inconsistencies within deployer itself, you can run the diagnostics mode. For example:

```
 $ docker run --rm -it tapis/deployer-input-gen -d
 ```

This will print a report to the screen of various errors and warnings associated with the templates (both `inputgen` and `deploygen` templates). The following checks are performed:

  * Can all inputgen yaml files be loaded (as yaml)?
  * Are all required/recommended properties supplied in the yamls?
  * Are there any "todo"s in the text of the properties?
  * Can all the templates used by tapis-api-generator.py (i.e., `deployergen`) be loaded as jinja2 templates?
  * Are all variables needed by `deployergen` templates listes as inputs in the `inputgen` variables?