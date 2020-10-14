import boto3
import click
import json
import time


@click.group("cli")
def cli():
    """
    Export and import AWS SSM Parameter Store values
    """

@cli.command("download")
@click.option('--path', 
                default='/', 
                help='The path of the parameters to download. Leave blank for "/"')
@click.option('--region', 
                prompt='AWS region',
                help='The region you want to pull parameters from')
def download_parameters(path, region):
    filename = f"params_{region}_{time.strftime('%d%m%y_%H%M')}.txt"
    next_token = ' '    
    while next_token is not None:
        response = get_parameters(path, next_token, region)
        for param in response['Parameters']:
            with open(filename, "a") as f: 
                f.write(f"{json.dumps(param, default=str)}\n") 
        next_token = response.get('NextToken', None)


@cli.command("upload")
@click.option('--filename', prompt='Filename', help='The parameters file to upload')
@click.option('--region', prompt='AWS region', help='The region you want to push parameters to')
def upload_parameters(filename, region):
    client = boto3.client('ssm', region)
    f = open(filename, "r")
    for param in f:
        dict_param = json.loads(param)
        response = client.put_parameter(
            Name=dict_param['Name'],
            Type=dict_param['Type'],
            Value=dict_param['Value'],
            DataType=dict_param['DataType']
        )
        click.echo(response)


def get_parameters(path, next_token, region):
    client = boto3.client('ssm', region)
    response = client.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True,
        MaxResults=10,
        NextToken=next_token)
    return response

if __name__ == '__main__':
    cli()