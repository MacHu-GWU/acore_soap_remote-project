
.. image:: https://readthedocs.org/projects/acore-soap-remote/badge/?version=latest
    :target: https://acore-soap-remote.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_soap_remote-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_soap_remote-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_soap_remote-project

.. image:: https://img.shields.io/pypi/v/acore-soap-remote.svg
    :target: https://pypi.python.org/pypi/acore-soap-remote

.. image:: https://img.shields.io/pypi/l/acore-soap-remote.svg
    :target: https://pypi.python.org/pypi/acore-soap-remote

.. image:: https://img.shields.io/pypi/pyversions/acore-soap-remote.svg
    :target: https://pypi.python.org/pypi/acore-soap-remote

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-soap-remote.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-soap-remote.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_remote-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-soap-remote#files


Welcome to ``acore_soap_remote`` Documentation
==============================================================================
.. image:: https://acore-soap-remote.readthedocs.io/en/latest/_static/acore_soap_remote-logo.png
    :target: https://acore-soap-remote.readthedocs.io/en/latest/

在阅读本项目文当前, 请先阅读 `acore_soap-project <https://github.com/MacHu-GWU/acore_soap-project>`_ 的 README 的第一段来了解 acore soap 系列项目的背景.

该项目提供了一套开发者工具. 它对用 Run Command Service 远程执行 CLI 的业务逻辑进行了封装, 并且做出了很多优化, 例如利用 AWS S3 储存输入和输出结果, 以应对批量执行大量命令的情况, 还例如非常高级的异常处理. 基于这套 SDK, 开发者可以很容易地开发出远程执行 GM 命令的应用程序, 将其嵌入到魔兽世界服务器管理后台中.


.. _install:

Install
------------------------------------------------------------------------------

``acore_soap_remote`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-soap-remote

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-soap-remote
