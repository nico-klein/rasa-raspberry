# Playground Rasa on a Raspberry Pi connected to Alexa
## ubuntu 20.04 / python 3.8 / tensorflow 2.3 / rasa 2.3
It's only a test project to get RASA running on a raspberry pi and connect to an Alexa Skill.
It works also with win 10 or macos 

# Install a raspberry pi
I didn't found all needed packages for the raspberry pi to get rasa running. That's why I build tensorflow with text and addons myself.

* base image: ubuntu-20.04.2-preinstalled-server-arm64+raspi.img
* I used a raspberry pi 4 with 8 GB ram. This works fine

## some usefull settings 
* sudo dpkg-reconfigure keyboard-configuration
* sudo ufw allow ssh

## install libs
* sudo apt install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential 
libncursesw5-dev libc6-dev openssl git
* sudo apt-get install libopenblas-base libblas-dev liblapack-dev cython libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev
* sudo apt-get install pkg-config libhdf5-dev
* sudo apt-get install libpq-dev

## create python venv
* sudo apt-get install python3-venv 
* python3 -m venv /home/ubuntu/rasa1/venv
* source ./rasa1/venv/bin/activate

# build and install tensorflow 
## install bazel 
* see https://github.com/PINTO0309/Bazel_bin
* https://github.com/PINTO0309/Bazel_bin/blob/main/3.7.2/aarch64/install.sh

## build tensorflow 2.3 (venv activated)
* the build takes a long time on the raspberry (>10 hours)
* see also https://www.tensorflow.org/install/source
* git clone https://github.com/tensorflow/tensorflow.git
* cd tensorflow
* git checkout r2.3
* ./configure
* bazel build -c opt --local_ram_resources=4096  --local_cpu_resources=HOST_CPUS*.5 --config=noaws --copt="-funsafe-math-optimizations" --copt="-ftree-vectorize" --copt="-fomit-frame-pointer" --verbose_failures tensorflow/tools/pip_package:build_pip_package
* so not use:  not --copt="-mfpu=neon-vfpv4"
* bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
* copy created wheel to folder of choice
* pip3 uninstall tensorflow
* pip3 install tensorflow-2.3.1-cp38-cp38-linux_aarch64.whl
* ? pip3 install keras_applications==1.0.8 --no-deps
* ? pip3 install keras_preprocessing==1.1.0 --no-deps
* ? pip3 install h5py==2.9.0
* ? pip3 install pybind11
* ? pip3 install -U ser six wheel mock

##build tensorflow-text  (venv activated)
* see also https://github.com/tensorflow/text
* git clone https://github.com/tensorflow/text.git
* cd text
* git checkout 2.3
* ./oss_scripts/run_build.sh
* copy created wheel to folder of choice
* pip3 install  tensorflow_text-2.3.0-cp38-cp38-linux_aarch64.whl

## build tensorflow addons  (venv activated)
* git clone https://github.com/tensorflow/addons.git
* cd addons/
* git checkout r0.11
* python3 ./configure.py
* bazel build build_pip_pkg
* bazel-bin/build_pip_pkg artifacts
* copy created wheel to folder of choice
* pip3 install tensorflow_addons-0.11.2-cp38-cp38-linux_aarch64.whl 

# install rasa
* pip3 install rasa==2.3.4
* You start rasa with custom python script if rasa returns errors with scikit-learn. 
   * insert in rasa start-script (in /venv/bin/): import sklearn
  
# install rasa x
* pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
* if problems on mac you could try: pip install --upgrade pip==20.2 
* start with rasa x (will start rasa x on port 5002 and rasa server on port 5005 but not actions server)
* windows only: if rasa x starts with errors encoding and utf-8 _>  set PYTHONUTF8=1

# create sqlite db to log coversations
* can be created but rasa will create one if not there when starting server 
  (e.g. in folder of bot: sqlite3 bot1.sqlite)
* add entry in endpoints.yml

# install ngrok if you want to connect to alexa skill
* sudo snap install ngrok
* If you create a free account you can get a token and will not have the 2 hour limitation

# connect to Alexa
* see the very good description and video https://blog.rasa.com/connect-your-rasa-ai-assistant-to-amazon-alexa/
* POST from alexa go to http://server:5005/webhooks/alexa_assistant/webhook
* check status with http://server::5005/webhooks/alexa_assistant

# spacy and other language
* pip install spacy
* python -m spacy download de_dep_news_trf
* python -m spacy download de_core_news_sm

# proxy (windows)
* rasa action server could have problems to connect rasa x with activated proxy
  set http_proxy=
  set https_proxy=

# python 
* freeze current installtion settings e.g. : python -m pip freeze >requirements_rasa25.txt

# ports
* rasa server   : 5005 ( check with http://server:5005/version )
* action server : 5055
* rasa x        : 5002 (default with password. see when rasa x has started)