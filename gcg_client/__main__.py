import requests
import json
import argparse
from datetime import datetime
import time

parser = argparse.ArgumentParser(description='Genesis Configuration Generator client')

parser.add_argument('--host', help='hostname or IP address used for the GCG API session.')
parser.add_argument('--port', help='Port number used in the Genesis API REST calls')
parser.add_argument('--timeout', help='Timeout for request')
parser.add_argument('--return_type', default='text', help='Timeout for request')
parser.add_argument('--json', required=True, help='JSON file used as data payload for GCG REST Call.')
# parser.add_argument('--template_type', required=True, help='Template type used to generate configuration file.')

aws_arg_group = parser.add_argument_group('aws_arg_group')
aws_arg_group.add_argument('--aws_key_id', help='AWS key id for S3 storage')
aws_arg_group.add_argument('--aws_secret_key', help='AWS secret key for S3 storage')
aws_arg_group.add_argument('--aws_bucket_id', help='AWS Bucket for S3 storage')
aws_arg_group.add_argument('--store_aws',
                           help='AWS Bucket for S3 storage, if True, remember to set the name of the file as the name will be over written. ',
                           action='store_true')
aws_arg_group.add_argument('--name', help='File name to store config is AWS bucket')
aws_arg_group.add_argument('--lab_name', help='Lab name associated with config file.')


class LCGClient:

    def __init__(self, host='127.0.0.1', port=5002, **kwargs):
        self._host = host
        self._port = str(port)
        self.aws_key_id = kwargs.get("aws_key_id")
        self.aws_secret_key = kwargs.get("aws_secret_key")
        self.aws_bucket_id = kwargs.get("aws_bucket_id")
        self._endpoint = kwargs.get("endpoint", '/api/v1/gcg')

        self._url = None

    def gen_base_config(self, data, **kwargs):

        opts = data.get("opts")

        if not opts.get("name"):
            opts['name'] = f'GCG_CLIENT_{str(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))}'

        if not opts.get("lab_name"):
            opts['lab_name'] = f'GCG_CLIENT_{str(datetime.now().strftime("%m_%d_%Y"))}'

        if not opts.get("store_aws"):
            opts['store_aws'] = kwargs.get("store_aws", False)

        self._url = f'http://{self._host}:{self._port}{self._endpoint}?return_type={kwargs.get("return_type")}'

        resp = requests.post(
            url=f'{self._url}',
            headers={'Content-Type': "application/json"},
            data=json.dumps(data)
        )
        return resp.text


def main():
    cli_args = parser.parse_args()

    json_file_name = cli_args.json

    with open(json_file_name, 'r') as file:
        data = json.load(file)

    aws_key_id = cli_args.aws_key_id or None
    aws_secret_key = cli_args.aws_secret_key or None
    aws_bucket_id = cli_args.aws_bucket_id or None
    #
    store_aws = cli_args.store_aws or False
    name = cli_args.name or None
    port = cli_args.port or '5000'
    host = cli_args.host or 'ec2-18-224-56-249.us-east-2.compute.amazonaws.com'
    return_type = cli_args.return_type

    client = LCGClient(
        host=host,
        port=port,
        aws_key_id=aws_key_id,
        aws_secret_key=aws_secret_key,
        aws_bucket_id=aws_bucket_id,
    )

    response = client.gen_base_config(
        data=data,
        store_aws=store_aws,
        host=host,
        port=port,
        name=name,
        return_type=return_type
    )

    print(response)


if __name__ == "__main__":
    main()
