How it Works
==============================================================================


Overview
------------------------------------------------------------------------------
:func:`~acore_soap_remote.request.run_soap_command` 是 SDK 的核心函数, 它可以将 GM 命令从任何地方, 例如 EC2, ECS, Lambda, 或是本地电脑, 发送到游戏服务器上运行, 并获得返回的结果. 这个函数的底层实现是 build 好 `acoresoapagent gm ... <https://acore-soap-agent.readthedocs.io/en/latest/acore_soap_agent/cli/main.html#acore_soap_agent.cli.main.Command.gm>`_ 所需要的 CLI 命令, 然后使用 `aws_ssm_run_command <https://github.com/MacHu-GWU/aws_ssm_run_command-project>`_ 这个库远程执行这个 CLI. 根据你的参数, 你可以选 SOAP response 打印到 stdout 或是写入到 S3. 注意, 这个函数仅仅是开始一个异步执行, 它不会自动等待执行完成, 而是会返回一个 :class:`~acore_soap_remote.request.SoapResponseAsyncGetter` 对象. 这个对象有一个 :meth:`~acore_soap_remote.request.SoapResponseAsyncGetter.get` 方法, 你可以调用这个方法来等待执行完成并获得对应的 `SOAPResponse <https://acore-soap.readthedocs.io/en/latest/acore_soap/request.html#acore_soap.request.SOAPResponse>`_ 的列表.


Usage Example
------------------------------------------------------------------------------
`test_request <https://github.com/MacHu-GWU/acore_soap_remote-project/blob/main/tests_int/test_request.py>`_ 这个例子展示了如何使用 ``run_soap_command`` 函数.

.. dropdown:: test_request.py

    .. literalinclude:: ../../../tests_int/test_request.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:
