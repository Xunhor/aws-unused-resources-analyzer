import boto3
from botocore.exceptions import ClientError
import datetime

# Cliente EC2
ec2 = boto3.client('ec2')
# Cliente RDS
rds = boto3.client('rds')
# Cliente ELB
elb = boto3.client('elbv2')
# Cliente S3
s3 = boto3.client('s3')
# Cliente ECS
ecs = boto3.client('ecs')

def listar_volumes_nao_anexados():
    try:
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
        if not volumes:
            print("Nenhum volume não anexado encontrado.")
        for volume in volumes:
            print(f"Volume não anexado: {volume['VolumeId']}")
    except ClientError as e:
        print(f"Erro ao listar volumes: {e}")

def listar_instancias_paradas():
    try:
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        stopped_instances = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
        
        if not stopped_instances:
            print("Nenhuma instância EC2 parada encontrada.")
        for instance_id in stopped_instances:
            print(f"Instância EC2 parada: {instance_id}")
    except ClientError as e:
        print(f"Erro ao listar instâncias: {e}")

def listar_snapshots_nao_referenciados():
    try:
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        unused_snapshots = [snapshot['SnapshotId'] for snapshot in snapshots if snapshot['VolumeId'] is None]
        
        if not unused_snapshots:
            print("Nenhum snapshot não referenciado encontrado.")
        for snapshot_id in unused_snapshots:
            print(f"Snapshot não referenciado: {snapshot_id}")
    except ClientError as e:
        print(f"Erro ao listar snapshots: {e}")

def listar_load_balancers_nao_utilizados():
    try:
        load_balancers = elb.describe_load_balancers()['LoadBalancers']
        unused_load_balancers = []
        
        for lb in load_balancers:
            if lb['State']['Code'] == 'active':
                listeners = elb.describe_listeners(LoadBalancerArn=lb['LoadBalancerArn'])
                if not listeners['Listeners']:
                    unused_load_balancers.append(lb['LoadBalancerArn'])
        
        if not unused_load_balancers:
            print("Nenhum load balancer não utilizado encontrado.")
        for lb_arn in unused_load_balancers:
            print(f"Load balancer não utilizado: {lb_arn}")
    except ClientError as e:
        print(f"Erro ao listar load balancers: {e}")

def listar_buckets_s3_vazios():
    try:
        buckets = s3.list_buckets()['Buckets']
        empty_buckets = []
        
        for bucket in buckets:
            objects = s3.list_objects_v2(Bucket=bucket['Name'])
            if 'Contents' not in objects:
                empty_buckets.append(bucket['Name'])
        
        if not empty_buckets:
            print("Nenhum bucket S3 vazio encontrado.")
        for bucket_name in empty_buckets:
            print(f"Bucket S3 vazio: {bucket_name}")
    except ClientError as e:
        print(f"Erro ao listar buckets S3: {e}")

def listar_ips_elasticos_nao_utilizados():
    try:
        elastic_ips = ec2.describe_addresses()['Addresses']
        unused_ips = [ip['PublicIp'] for ip in elastic_ips if 'InstanceId' not in ip]
        
        if not unused_ips:
            print("Nenhum IP elástico não utilizado encontrado.")
        for ip in unused_ips:
            print(f"IP elástico não utilizado: {ip}")
    except ClientError as e:
        print(f"Erro ao listar IPs elásticos: {e}")

def listar_tarefas_e_clusters_ecs_nao_utilizados():
    try:
        clusters = ecs.list_clusters()['clusterArns']
        unused_clusters = []
        
        for cluster in clusters:
            tasks = ecs.list_tasks(cluster=cluster)
            if not tasks['taskArns']:
                unused_clusters.append(cluster)
        
        if not unused_clusters:
            print("Nenhum cluster ECS não utilizado encontrado.")
        for cluster in unused_clusters:
            print(f"Cluster ECS não utilizado: {cluster}")
    except ClientError as e:
        print(f"Erro ao listar clusters ECS: {e}")

# Executar funções
listar_volumes_nao_anexados()
listar_instancias_paradas()
listar_snapshots_nao_referenciados()
listar_load_balancers_nao_utilizados()
listar_buckets_s3_vazios()
listar_ips_elasticos_nao_utilizados()
listar_tarefas_e_clusters_ecs_nao_utilizados()
