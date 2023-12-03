# mus

[Wise mouse in the haystack](https://docs.google.com/document/d/12PTVOyS4rCeGe4xmUxWdnA-8ibMU4Zw7rrc8bfp5kZA/edit?usp=sharing)

## Silos to text pipeline

````
# set virtualenv
virtualenv -p python3.10 .venv
source .venv/bin/activate
pip install -r requirements/requirements_data.txt

/media/vola/mus_std/bin/es/elasticserach
# /media/vola/mus_std/bin/cerebro/cerebro or kibana

# run from project root directory run_* to get help:
python run_cleansing.py

Usage: run_cleansing.py [OPTIONS] COMMAND [ARGS]...

  Data cleansing runner

Options:
  --help  Show this message and exit.

Commands:
  extract_text_json  Extract unstructured archive text with metadata
  get_json_text      Extract text from json into silos
  index_json_text    Index jsom archive text
````

Extract text, run topic modeling and NER

````
# extract text from silos archive
python run_arc_walk.py extract_text_json -a /media/vola/mus_row/_1_ -t /media/vola/mus_std/_1_cln/

# topic modeling and NER 
python run_topic.py model_topic -t /media/vola/mus_std/_1_std/ --update --per_subdir -l ru -l ua -l en

# create new index (elaticstarch)
python run_arc_walk.py index_json_text -t /media/vola/mus_std/_1_std/ --ci

try:
arc_text/_search
{
  "query": {
    "match": {"text": "склад" }
  },
  "_source": ["file_path", "text", "topics", "named_entities"]
}

{
  "size": 0,
  "aggs": {
    "topics_term_count": {
      "terms": {"field": "topics"}
    }
  }
}

{
  "size": 0,
  "aggs": {
    "word_frequency": {
      "terms": {"field": "text"}
    }
  }
}
````

Chat

````
# create text db to chat with via LLM
python run_arc_walk.py get_json_text -t /media/vola/mus_std/_1_std/ -d /media/vola/mus_std/gpt_text/ 

H2OGPT (not stable)
cd /media/vola/mus_std/bin
git clone https://github.com/h2oai/h2ogpt.git
cd h2ogpt
virtualenv -p python3.10 .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/make_db.py --user_path="/media/vola/mus_std/gpt_text/" --collection_name=VOLAData --selected_file_types="['txt']"
python generate.py --base_model='llama' --prompt_type=llama2 --score_model=None --max_max_new_tokens=2048 --max_new_tokens=1024 \
       --visible_tos_tab=False --visible_hosts_tab=False --visible_models_tab=False \
       --langchain_modes="['LLM','PersistData']" --langchain_mode=PersistData \
       --langchain_mode_types="{'PersistData':'shared'}" \
       --top_k_docs=-1 --max_time=360 --save_dir=save \
       --model_path_llama=https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q6_K.gguf \
       --max_seq_len=4096

LOCALGPT
git clone https://github.com/PromtEngineer/localGPT.git
cd localGPT
virtualenv -p python3.10 .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install llama-cpp-python==0.1.83

SOURCE_DOCUMENTS=/media/vola/mus_std/gpt_text/
MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"

python ingest.py

python run_localGPT.py
or
python run_localGPT_API.py

````

### Repository structures

- scripts - shell scrips (temporary to support ec2 env deploy)
- mus - project package name, nlp tasks implementation example
- requirements - python requirements files
- run*.py - commands to run nlp tasks

### Development convention

- use python v. 3.10;
- use [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) as coding convention;
- use pytest as project test framework, test coverage: standard input and corner cases, exception/IO errors;
- use pylint for code style check, requirement: 0 warnings;
- use mypy for static code check, requirement: 0 warnings.
- be a team player, commit, participate
  in [code review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- see & learn [examples](https://github.com/run-llama/llama_index)

### Branching strategy

Please use [git workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) convention while
development.

We use simplified gitflow process.

Branches:

```master``` - production code branch

```develop``` - development default branch

Branch naming convention:

```<task_num>-short-description```

Commit comment convention:  
```<task_num> | short description```

<task_num> is a git issue (task) number

Development flow example;

```
# checkout locally to the develop branch & pull last changes
git checkout develop
git pull

# create new bracnh from develop, 
git checkout -b 2-update-requirements

# create & edit & coding
# usable git command: git status, git stash, git stash apply etc.
git status
# Please use git "add ." if you are confident there are only 
# required files in the commit will be used
git add .
# or 
git add <file1> <file2>

git commit -m "2 | updated reqirements"
git push origin 2-update-requirements
# create pull requiest, review, merge, cleanup

git checkout develop
git branch -d 2-update-requirements
```

### Local development environment

Please use [virtualenv|https://docs.python.org/3.10/library/venv.html] for local development.

e.g.

- Install virtualenv & dependencies, Linux

```
cd my-project
virtualenv -p python3.10 .venv
source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements/requirements_dev.txt

```

- Install virtualenv & dependencies, Windows

```
python --version
# Python 3.10.13
pip install virtualenv
cd my-project
virtualenv --python C:\Path\To\Python\python3.10.exe .venv
.venv/bin/activate
pip install -r requirements/requirements_dev.txt
```

- Run tests

```
source .venv/bin/activate
pytest
```

- Run code style and type checks

```
source .venv/bin/activate
pylint project_package_name*
mypy project_package_name*
```

## CI/CD & docker builds

### Docker build

- set Environment variables

(TODO: fix after implementation)

- build container & run:

```
docker build .
```
