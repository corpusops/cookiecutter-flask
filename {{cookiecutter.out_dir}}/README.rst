{{cookiecutter.lname}}
{{cookiecutter.lname|length * '=' }}

.. contents::


Initialise your development environment
***************************************

All following commands must be run only once at project installation.


First clone
-----------

.. code-block:: sh

    git clone --recursive {{cookiecutter.git_project_url}}
    {%if cookiecutter.use_submodule_for_deploy_code-%}git submodule init # only the fist time
    git submodule update --recursive{%endif%}


Before using any ansible command: a note on sudo
---------------------------------------------------
If your user is ``sudoer`` but is asking for you to input a password before elavating privileges,
you will need to add ``--ask-sudo-pass`` and maybe ``--become`` to any of the following ``ansible alike`` commands.


Install docker and docker compose
----------------------------------
if you are under debian/ubuntu/mint/centos you can do the following:

.. code-block:: sh

    .ansible/scripts/download_corpusops.sh
    .ansible/scripts/setup_corpusops.sh
    local/*/bin/cops_apply_role --become \
        local/*/*/corpusops.roles/services_virt_docker/role.yml

... or follow official procedures for `docker <https://docs.docker.com/install/#releases>`_ and  `docker-compose <https://docs.docker.com/compose/install/>`_.

Update corpusops
------------------

You may have to update corpusops time to time with:
￼

.. code-block:: sh

    ./control.sh up_corpusops

Configuration
----------------

Use the wrapper to init configuration files from their ``.dist`` counterpart
and adapt them to your needs.

.. code-block:: sh

    ./control.sh init

Login to the app docker registry
-----------------------------------

You need to login to our docker registry to be able to use it:

.. code-block:: sh

    docker login {{cookiecutter.docker_registry}}  # use your gitlab user

{%- if cookiecutter.registry_is_gitlab_registry %}
**⚠️ See also ⚠️** the
    `project docker registry`<{{cookiecutter.git_project_url.replace('ssh://', 'https://').replace('git@', '')}}/container_registry>_
{%- else %}

**⚠️ See also ⚠️** the makinacorpus doc in the docs/tools/dockerregistry section.
{%- endif%}

Use your development environment
+++++++++++++++++++++++++++++++++

Update submodules
-----------------
Never forget to grab and update regulary the project submodules:

.. code-block:: sh

    git pull{% if cookiecutter.use_submodule_for_deploy_code
    %}
    git submodule init # only the fist time
    git submodule update --recursive{%endif%}

Control.sh helper
-------------------
You may use the stack entry point helper which has some neat helpers but feel
free to use docker command if you know what your are doing.

.. code-block:: sh

    ./control.sh usage # Show all available commands

Start the stack
----------------

After a last verification of the files, to run with docker, just type:

.. code-block:: sh

    # First time you download the app, or sometime to refresh the image
    ./control.sh pull # Call the docker compose pull command
    ./control.sh up # Should be launched once each time you want to start the stack

Launch app as foreground
-------------------------

.. code-block:: sh

    ./control.sh fg

**⚠️ Remember ⚠️** to use **./control.sh up** to start the stack before.


Run plain docker-compose commands
------------------------------------

- Please remember that the ``CONTROL_COMPOSE_FILES`` env var controls which docker-compose configs are use (list of space separated files), by default it uses the dev set.

    .. code-block:: sh

        ./control.sh dcompose <ARGS>


Start a shell inside the {{cookiecutter.app_type}} container
------------------------------------------------------------------

- for user shell

    .. code-block:: sh

        ./control.sh usershell

- for root shell

  .. code-block:: sh

        ./control.sh shell

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

Rebuild/Refresh local docker image in dev
------------------------------------------------

  .. code-block:: sh

    ./control.sh buildimages

Running heavy session
------------------------------------------------

Like for installing and testing packages without burning them right now in requirements.<br/>
You will need to add the network alias and maybe stop the flask worker

    .. code-block:: sh

        ./control.sh stop {{cookiecutter.app_type}}
        services_ports=1 ./control.sh usershell
        flask run

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

Use flask tool (eg: run/shell/routes)
*************************************
Just as easy as

    .. code-block:: sh

        ./control.sh flask $args

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

Run tests
************

.. code-block:: sh

    ./control.sh tests
    # also consider:
    ./control.sh linting
    ./control.sh coverage

**⚠️ Remember ⚠️** to use **./control.sh up** to start the stack before.


File permissions
*****************
If you get annoying file permissions problems on your host in development, you can use the following routine to (re)allow your host
user to use files in your working directory


.. code-block:: sh

    ./control.sh open_perms_valve


Docker volumes
****************

Your application extensivly use docker volumes. From times to times you may
need to erase them (eg: burn the db to start from fresh)

.. code-block:: sh

    docker volume ls  # hint: |grep \$app
    docker volume rm $id


Refresh Pipenv.lock
**********************

.. code-block:: sh

    ./control.sh usershell "cd requirements && pipenv lock"


Reusing a precached image in dev to accelerate rebuilds
*******************************************************
Once you have build once your image, you have two options to reuse your image as a base to future builds, mainly to accelerate buildout successive runs.

- Solution1: Use the current image as an incremental build: Put in your .env

    .. code-block:: sh

        FLASK_BASE_IMAGE=registry.makina-corpus.net/mirabell/chanel:latest-dev

- Solution2: Use a specific tag: Put in your .env

    .. code-block:: sh

        FLASK_BASE_IMAGE=a tag
        # this <a_tag> will be done after issuing: docker tag registry.makina-corpus.net/mirabell/chanel:latest-dev a_tag

Integrating an IDE
*******************
- **DO NOT START YET YOUR IDE**
- Add to your .env and re-run ``./control.sh build flask``

    .. code-block:: sh

        WITH VISUALCODE=1
        #  or
        WITH_PYCHARM=1
        # note that you can also set the version to install (see .env.dist)

- Start the stack, but specially stop the app container as you will
  have to separatly launch it wired to your ide

    .. code-block:: sh

        ./control.sh up
        ./control.sh down flask


Get the completion and the code resolving for bundled dependencies wich are inside the container
-------------------------------------------------------------------------------------------------

- Whenever you rebuild the image, you need to refresh the files for your IDE to complete bundle dependencies

    .. code-block:: sh

        ./control.sh get_container_code

Using pycharm
-----------------
- Only now launch pycharm and configure a project on this working directory
- Whenever you open your pycharm project:
    - Add local/code/venv/lib/python*/site-packages to sources if it is not already

Make a break, insert a PDB and attach the session on Pycharm
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
- The docker container will connect to your running pycharm process, using a network tcp connection, eg on port ``12345``.
- ``12345`` can be changed but of course adapt the commands, this port must be reachable from within the container.
- Linux only: This iptables rule can be more restrictive if you know and you want to but as the following it will allow unfiltered connections on port ``12345``.

    .. code-block:: sh

        iptables -I INPUT  -p tcp -m tcp --dport 12345 -j ACCEPT

- Ensure you added ``WITH_PYCHARM`` in your ``.env`` and that ``PYCHARM_VERSION`` is tied to your PYCHARM installation and start from a fresh build if it was not (pip will mess to update it correctly, sorry).
- Wherever you have the need to break, insert in your code the following snippet:

    .. code-block:: python

        import pydevd_pycharm;pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)

    - if ``host.docker.internal`` does not work for you, you can replace it by the local IP of your machine.
- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.
  Eg: if  you want to put a pdb in ``six.py``

    - DO NOT DO IT in ``local/code/**/six.py``

        .. code-block:: sh

            ./control.sh down flask
            services_ports=1 ./control.sh usershell
            apt install -y vim
            vim **/six.py
            # insert: import pydevd_pycharm;pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)
            python src/*/api.py

    - With pycharm and your configured debugging session, attach to the session


Using VSCode
------------
- You must launch VSCode using ``./control.sh vscode`` as vscode needs to have the ``PYTHONPATH`` variable preset to make linters work

    .. code-block:: sh

        ./control.sh vscode

- In other words, this add ``local/**/site-packages`` to vscode sys.path.
- Additionnaly, adding this to ``.vscode/settings.json`` would help to give you a smooth editing experience

    .. code-block:: json

        {
          "files.watcherExclude": {
              "**/.git/objects/**": true,
              "**/.git/subtree-cache/**": true,
              "**/node_modules/*/**": true,
              "**/local/*/**": true,
              "**/local/code/venv/lib/**/site-packages/**": false

            }
        }

Debugging with VSCode
+++++++++++++++++++++
- `vendor documentation link <https://code.visualstudio.com/docs/python/debugging#_remote-debugging>`_
- The VSCode process will connect to your running docker container, using a network tcp connection, eg on port ``5678``.
- ``5678`` can be changed but of course adapt the commands, this port must be reachable from within the container and in the ``docker-compose-dev.yml`` file.
- Ensure you added ``WITH_VSCODE`` in your ``.env`` and that ``VSCODE_VERSION`` is tied to your VSCODE installation and start from a fresh build if it was not (pip will mess to update it correctly, sorry).
- Wherever you have the need to break, insert in your code the following snippet after imports (and certainly before wherever you want your import):

    .. code-block:: python

        import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()

- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.
  Eg: if  you want to put a pdb in ``six.py``

    - DO NOT DO IT in ``local/code/**/six.py``
    - do:

        .. code-block:: sh

            ./control.sh down flask
            services_ports=1 ./control.sh usershell
            apt install -y vim
            vim **/six.py
            # insert: import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()
            python src/*/api.py

- toggle a breakpoint on the left side of your text editor on VSCode.
- Switch to Debug View in VS Code, select the Python: Attach configuration, and select the settings (gear) icon to open launch.json to that configuration.
  Duplicate the remote attach part and edit it as the following

    .. code-block:: json

        {
          "name": "Python Docker Attach",
          "type": "python",
          "request": "attach",
          "pathMappings": [
            {
              "localRoot": "${workspaceFolder}",
              "remoteRoot": "/code"
            }
          ],
          "port": 5678,
          "host": "localhost"
        }

- With VSCode and your configured debugging session, attach to the session and it should work


Doc for deployment on environments
**********************************
- `See here <./docs/deploy.md>`_.

FAQ
****
{% if cookiecutter.with_nginx %}
If you get troubles with the nginx docker env restarting all the time, try recreating it

.. code-block:: sh

    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d --no-deps --force-recreate nginx backup
{% endif %}

If you get the same problem with the flask docker env

.. code-block:: sh

    docker-compose -f docker-compose.yml -f docker-compose-dev.yml stop flask db
    docker volume rm oppm-postgresql # check with docker volume ls
    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d db
    # wait fot postgis to be installed
    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up flask
