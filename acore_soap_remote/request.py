# -*- coding: utf-8 -*-

"""
这是 SDK 的核心模块, 实现了各种底层方法.
"""

import typing as T
import time
import json
import dataclasses

from func_args import NOTHING, resolve_kwargs
import aws_ssm_run_command.api as aws_ssm_run_command
from acore_soap.api import (
    SOAPRequest,
    SOAPResponse,
)

from .paths import path_agent_cli
from .utils import get_object, put_object

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3.client import S3Client
    from mypy_boto3_ssm.client import SSMClient


def upload_requests_to_s3(
    requests: T.List[SOAPRequest],
    s3_client: "S3Client",
    s3uri: str,
):
    put_object(
        s3_client=s3_client,
        s3uri=s3uri,
        body=json.dumps([request.to_dict() for request in requests]),
    )


def build_cli_arg_for_gm(
    command: str,
    username: T.Optional[str] = None,
    password: T.Optional[str] = None,
    host: T.Optional[str] = None,
    port: T.Optional[int] = None,
    raises: bool = True,
    output_s3uri: T.Optional[str] = None,
    path_agent_cli: str = path_agent_cli,
) -> str:
    """
    构造最终的命令行参数. 以便之后 pass 给 ``acoresoapagent gm ...`` CLI 命令.
    """
    args = [
        path_agent_cli,
        "gm",
        f'"{command}"',
    ]
    if username is not None:
        args.append(f"--user={username}")
    if password is not None:
        args.append(f"--pwd={password}")
    if host is not None:
        args.append(f"--host={host}")
    if port is not None:
        args.append(f"--port={port}")
    if raises is not None:
        if raises:
            args.append(f"--raises=True")
        else:
            args.append(f"--raises=False")
    if output_s3uri is not None:
        args.append(f"--s3uri={output_s3uri}")
    return " ".join(args)


@dataclasses.dataclass
class SoapResponseAsyncGetter:
    """
    A helper class to get SOAP responses asynchronously.
    """

    command_id: str = dataclasses.field()
    ec2_instance_id: str = dataclasses.field()
    ssm_client: "SSMClient" = dataclasses.field()
    output_s3uri: T.Optional[str] = dataclasses.field()
    s3_client: T.Optional["S3Client"] = dataclasses.field()
    delays: int = dataclasses.field()
    timeout: int = dataclasses.field()
    verbose: bool = dataclasses.field()

    def get(self) -> T.List[SOAPResponse]:
        """
        Wait until the command is completed, and return all soap response.
        """

        # sync mode, wait until command succeeded
        time.sleep(1)

        # get command response
        command_invocation = (
            aws_ssm_run_command.better_boto.wait_until_send_command_succeeded(
                ssm_client=self.ssm_client,
                command_id=self.command_id,
                instance_id=self.ec2_instance_id,
                raises=False,
                delays=self.delays,
                timeout=self.timeout,
                verbose=self.verbose,
            )
        )
        if command_invocation.ResponseCode != 0:
            raise aws_ssm_run_command.exc.RunCommandError.from_command_invocation(
                command_invocation
            )

        # parse response
        if self.output_s3uri is None:
            output = command_invocation.StandardOutputContent
            lines = output.splitlines()
            responses = [
                SOAPResponse.from_dict(json.loads(json_str)[0])
                for json_str in lines
            ]
        else:
            json_str = get_object(s3_client=self.s3_client, s3uri=self.output_s3uri)
            responses = [SOAPResponse.from_dict(dct) for dct in json.loads(json_str)]
        return responses


def run_soap_command(
    gm_commands: T.List[str],
    ec2_instance_id: str,
    ssm_client: "SSMClient",
    username: T.Optional[str] = None,
    password: T.Optional[str] = None,
    host: T.Optional[str] = None,
    port: T.Optional[int] = None,
    raises: bool = True,
    input_s3uri: T.Optional[str] = None,
    output_s3uri: T.Optional[str] = None,
    s3_client: T.Optional["S3Client"] = None,
    path_agent_cli: str = path_agent_cli,
    delays: int = 1,
    timeout: int = 10,
    verbose: bool = True,
) -> SoapResponseAsyncGetter:
    """
    从任何地方, 通过 SSM Run Command, 远程执行 SOAP 命令.

    - 如果显式指定了 ``s3uri_input``, 则将 GM 命令的输入写入 S3.
    - 如果显式指定了 ``s3uri_output``, 则将 GM 命令的输出写入 S3.
    - 如果没有显示指定 ``s3uri_output``, 有两种情况:
        1. requests 的数量不超过 20 条, 则将 GM 命令的输出作为 JSON 在 stdout 中打印,
            并在 ``ssm.send_command()`` API 返回.
        2. requests 的数量超过了 20 条, 则强制要求指定 ``s3uri_output`` 将 GM 命令的输出
            写入 S3.

    Usage Example:

    .. code-block:: python

        >>> response = run_soap_command(bsm, "sbx-blue", ".server info")
        >>> response = run_soap_command(bsm, "sbx-blue", [".account create test1 test1", ".account create test2 test2"])

    :param bsm: ``boto_session_manager.BotoSesManager`` 对象, 定义了 AWS 权限.
    :param gm_commands: 一组 GM 命令.
    :param request_like: 请参考
        :class:`~acore_soap_app.agent.impl.SOAPRequest.batch_load`
    :param username: 默认的用户名, 只有当 request.username 为 None 的时候才会用到.
    :param password: 默认的密码, 只有当 request.password 为 None 的时候才会用到.
    :param raises: 默认为 True. 如果为 True, 则在遇到错误时抛出异常. 反之则将
        failed SOAP Response 原封不动地返回.
    :param input_s3uri: 如果指定, 则将输入写入 S3. 常用于 Payload 比较大的情况.
        如果你一次性发送的 request 大于 20 条, 则必须使用这个参数.
    :param output_s3uri: 如果不指定, 则默认将输出作为 JSON 打印. 如果指定了 s3uri,
        则将输出写入到 S3.
    :param path_cli: EC2 上 acsoap 命令行工具的绝对路径.
    :param sync: 同步和异步模式, 默认为同步模式
        - 如果以同步模式运行, 则会等待 SSM Run Command 完成
        - 如果以异步模式运行, 则会立刻返回一个 SSM Run Command 的 command id.
    :param delays: 同步模式下的等待间隔
    :param timeout: 同步模式下的超时限制
    :param verbose: 同步模式下是否显示进度条
    """
    # validate args
    if (input_s3uri is not None) or (output_s3uri is not None):
        if s3_client is None:
            raise ValueError(
                "s3_client must be specified when s3uri_input is specified"
            )

    # identify the run strategy, send requests as it is or
    if len(gm_commands) >= 20:
        if input_s3uri is None:
            raise ValueError(
                "'s3uri_input' must be specified when the number of requests is greater than 20"
            )
        is_s3_input = True
    else:
        if input_s3uri is None:
            is_s3_input = False
        else:
            is_s3_input = True

    # prepare acoresoapagent cli command
    if is_s3_input:
        put_object(
            s3_client=s3_client,
            s3uri=input_s3uri,
            body=json.dumps(gm_commands),
        )
        commands = [
            build_cli_arg_for_gm(
                command=input_s3uri,
                username=username,
                password=password,
                host=host,
                port=port,
                raises=raises,
                output_s3uri=output_s3uri,
                path_agent_cli=path_agent_cli,
            )
        ]
    else:
        commands = [
            build_cli_arg_for_gm(
                command=gm_command,
                username=username,
                password=password,
                host=host,
                port=port,
                raises=raises,
                output_s3uri=output_s3uri,
                path_agent_cli=path_agent_cli,
            )
            for gm_command in gm_commands
        ]

    # run command
    command = aws_ssm_run_command.better_boto.run_shell_script_async(
        ssm_client=ssm_client,
        commands=commands,
        instance_ids=ec2_instance_id,
    )
    command_id = command.CommandId

    return SoapResponseAsyncGetter(
        command_id=command_id,
        ec2_instance_id=ec2_instance_id,
        ssm_client=ssm_client,
        output_s3uri=output_s3uri,
        s3_client=s3_client,
        delays=delays,
        timeout=timeout,
        verbose=verbose,
    )
