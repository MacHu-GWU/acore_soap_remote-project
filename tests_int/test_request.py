# -*- coding: utf-8 -*-

import boto3
from acore_server_metadata.api import Server
from acore_soap_remote.request import run_soap_command


def test():
    boto_ses = boto3.session.Session(profile_name="bmt_app_dev_us_east_1")
    ec2_client = boto_ses.client("ec2")
    rds_client = boto_ses.client("rds")
    s3_client = boto_ses.client("s3")
    ssm_client = boto_ses.client("ssm")

    server_id = "sbx-blue"
    server = Server(id=server_id)
    server.refresh(ec2_client=ec2_client, rds_client=rds_client)
    if server.is_running() is False:
        raise SystemError(f"EC2 {server_id!r} is not running")
    ec2_instance_id = server.ec2_inst.id

    # Run GM commands in sequence, and read the response data from stdout
    soap_response_async_getter = run_soap_command(
        gm_commands=[
            ".account delete test1",
            ".account create test1 1234",
            ".account set gmlevel test1 3 -1",
            ".account set password test1 123456 123456",
            ".account delete test1",
        ],
        ec2_instance_id=ec2_instance_id,
        ssm_client=ssm_client,
        s3_client=s3_client,
    )
    soap_response_list = soap_response_async_getter.get()
    for soap_response in soap_response_list:
        print("=" * 80)
        print(f"{soap_response.succeeded = }, {soap_response.message = }")

    # Run GM commands in sequence, and read the response data from S3
    soap_response_async_getter = run_soap_command(
        gm_commands=[
            ".account delete test1",
            ".account create test1 1234",
            ".account set gmlevel test1 3 -1",
            ".account set password test1 123456 123456",
            ".account delete test1",
        ],
        ec2_instance_id=ec2_instance_id,
        ssm_client=ssm_client,
        input_s3uri="s3://bmt-app-dev-us-east-1-data/projects/acore_soap_remote/int_test/input.json",
        output_s3uri="s3://bmt-app-dev-us-east-1-data/projects/acore_soap_remote/int_test/output.json",
        s3_client=s3_client,
    )
    soap_response_list = soap_response_async_getter.get()
    for soap_response in soap_response_list:
        print("=" * 80)
        print(f"{soap_response.succeeded = }, {soap_response.message = }")


if __name__ == "__main__":
    from acore_soap_remote.tests import run_cov_test

    run_cov_test(__file__, "acore_soap_remote.request", preview=False)
