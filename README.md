# Welcome to your new DBT project!
This template repo will help you get your DBT Project up and running in no time


## Requirements

### Clone Repo

Follow [this guide](https://wiki.tm8.dev/doc/git-hFhrzUByhS#h-setting-up-git-for-github) to setup your ssh keys then
clone the repository through ssh.

  ```sh
  git clone git@github.com:thinkingmachines/<this-repo>.git
  ```

### Python

1. Install `Python 3.8.12`

    - For **Ubuntu / Debian**

      ```sh
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt-get update
      sudo apt-get install python3.8
      ```

    - For **macOS**

      ```sh
      # Install pyenv
      brew update
      brew install pyenv
 
      # Run pyenv when launching zsh
      echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
      echo 'eval "$(pyenv init -)"' >> ~/.zshrc
 
      # Install Python 3.8.12
      pyenv install 3.8.12
      ```

   - For **Windows**, download installer from this [link](https://www.python.org/downloads/windows/)

2. Install `Poetry`

    - For **Linux** and **macOS**

      ```sh
      curl -sSL https://install.python-poetry.org | python3 -
      ```
      For **Windows**

      ```sh
      curl -sSL https://install.python-poetry.org | py -
      ```

    - Add Poetry to PATH by adding this snippet to `~/.bashrc` or `~/.zshrc` depending on your terminal of choice


      - For **Linux** and **macOS**
        ```sh
        export PATH=$PATH:$HOME/.local/bin
        ```

      Run `source ~/.bashrc` or the appropriate RC for `poetry` installation to take effect in terminal session.

      - For **Windows**

        ```sh
        set PATH=%PATH%;%USERPROFILE%\AppData\Roaming\Python\Scripts
        set PATH=%PATH%;%USERPROFILE%\AppData\Roaming\pypoetry\venv\Scripts
        ```

        This has to be run *every* time before using poetry

    - Check if installation was successful.

      ```sh
      poetry --version
      ```

## Install DBT dependencies
1. Change directory to where your cloned repository is. 

      ```sh
      cd <directory of cloned repository>
      ```
      
    This should contain the `pyproject.toml` file. Otherwise, initialize this directory using to create one:

    ```sh
    poetry init
    ```
2. Install dbt-core via poetry
   ```sh
   $ poetry add dbt-core
   ```

3. Add your prefered Data Warehouse (DWH) adapter (e.g. dbt-bigquery) to your list of dependencies via poetry. Refer to [dbt's list of verified adapters](https://docs.getdbt.com/docs/supported-data-platforms#verified-adapters)
   ```sh
   $ poetry add <dbt-adapter>
   ```
4. Install dependencies

    ```sh
    $ poetry install --with dev
    ```
5. Activate poetry shell (virtual env) and ensure that dbt is installed properly

    ```sh
    # Activate virtual environment
    $ poetry shell

    # Check dbt version
    (venv) $ dbt --version
    ```


## Initialize your DBT Project
### DBT Project
1. Open dbt_project.yml config file found in the root directory of your repo
2. Search and Replace all `dbt_starter` to the name of your repository/dbt-project.

### DBT Profile

#### Option 1:  
    
1. Make sure your dbt project is pointing the right PATH of your profiles config file by running this command

  For **Linux** or **macOS**:

    ```sh
    (venv) $ export DBT_PROFILES_DIR="./"
    ```

  For **Windows**:
  
    ```sh
    (venv) $ set DBT_PROFILES_DIR=<path to profiles directory>
    ```
    
2. Create a `profiles.yml` file by running the following command. DBT will prompt you with necessary information needed to connect your prefered DWH
    ```sh
    (venv) $ dbt init
    ```

3. Test your connection to your DWH
    ```sh
    (venv) $ dbt debug
    ```

#### Option 2: 
1. Rename `profiles.yml.sample` to `profiles.yml` and configure the necessary information.
	- [ ] In `line 1`, replace `project_directory` with the name of your repository.
	- [ ] Create a `dev` target as a default
	- [ ] `prod` target is only necessary if edit access to prod tables are needed. 

2. Make sure your dbt project is pointing the right PATH of your profiles config file by running this command
  
    For **Linux** or **macOS**:

      ```sh
      (venv) $ export DBT_PROFILES_DIR="./"
      ```

    For **Windows**:
    
      ```sh
      (venv) $ set DBT_PROFILES_DIR=<path to profiles directory>
      ```
    
3. Test your connection to your DWH
    ```sh
    (venv) $ dbt debug
    ```


**Note:** Your remote repo should have a dedicated profile.yml setup for prod use only. Each dev/user will have to create their own `profiles.yml` in their local repository. As such, profile.yml in your local repo should be added to the .gitignore file. Take this into account when building your DBT Projects


### Setting up your Data Layers
We have incorporated the [Data Modeling Workflow](https://wiki.tm8.dev/doc/data-modeling-workflow-0peVbGceor/edit) into the base model structure of this project. 

See the [models configuration](https://docs.getdbt.com/reference/model-configs) in `dbt_project.yml` to further configure the materializations and default target schemas of your data models.

See the [TM Enterprise Data Model](https://wiki.tm8.dev/doc/wip-tm-enterprise-data-model-hQUaeKGWWO) for a detailed overview on how to structure and name your schemas and models in dbt.


## Test your models
### Run unit tests against your models
1. Run all the models 
  ```sh
  (venv) $ dbt run
  ```
2. Run all the tests against the models
  ```sh
  (venv) $ dbt test
  ```
3. Change directory to ae_scripts 
  ```sh
  (venv) $ cd ae_scripts
  ```
4. Run the uat_tester.py file 
  ```sh
  (venv) $ python3 uat_tester.py
  ```
Once completed, it will print "Done" 

**Note:** The uat_tester.py must be run after running the tests (dbt test). 

### Export your tests
- Once the uat_tester.py file is ran, there will be a csv file under the seeds folder. 

## Generate a diagram for dbdiagram.io 
### Steps: 
1. Run all the models
  ```sh
  (venv) $ dbt run
  ```
2. Run the dbt documentation
  ```sh
  (venv) $ dbt docs generate
  ```
3. Change directory to ae_scripts 
  ```sh
  (venv) $ cd ae_scripts
  ```
3. Run the dbt_to_dbdiagram.py file 
  ```sh
  (venv) $ python3 dbt_to_dbdiagram.py
  ```
4. Paste the output in https://dbdiagram.io/

The resulting diagram will be grouped by schema. 

# Learning Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [DBT Best Practices](https://wiki.tm8.dev/doc/dbt-best-practices-ndIofcGpji) in the AE standpoint
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
