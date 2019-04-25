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
    {%-if cookiecutter.use_submodule_for_deploy_code%}git submodule init --recursive  # only the fist time
    git submodule upate{%endif%}

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

    git pull
    {%-if cookiecutter.use_submodule_for_deploy_code%}git submodule init --recursive  # only the fist time
    git submodule upate{%endif%}

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

    control.sh buildimages

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
    # also consider: linting|coverage

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

    ./control.sh usershell "pipenv lock && cat Pipfile.lock > Pipfile.lock.mounted"


Doc for deployment on environments
**********************************
- `See here <./docs/deploy.md>`_.

FAQ
****
If you get troubles with the nginx docker env restarting all the time, try recreating it

.. code-block:: sh

    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d --no-deps --force-recreate nginx backup

If you get the same problem with the flask docker env

.. code-block:: sh

    docker-compose -f docker-compose.yml -f docker-compose-dev.yml stop flask db
    docker volume rm oppm-postgresql # check with docker volume ls
    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d db
    # wait fot postgis to be installed
    docker-compose -f docker-compose.yml -f docker-compose-dev.yml up flask
