# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# Add comments
import re

# Environments (targeted at accounts)
DEPLOYMENT = 'Deployment'
DEV = 'Dev'
TEST = 'Test'
PROD = 'Prod'

# The following constants are used to map to parameter/secret paths
ENVIRONMENT = 'environment'

# Manual Inputs
GITHUB_REPOSITORY_OWNER_NAME = 'github_repository_owner_name'
GITHUB_REPOSITORY_NAME = 'github_repository_name'
ACCOUNT_ID = 'account_id'
REGION = 'region'
LOGICAL_ID_PREFIX = 'logical_id_prefix'
RESOURCE_NAME_PREFIX = 'resource_name_prefix'
VPC_CIDR = 'vpc_cidr'

# Secrets Manager Inputs
GITHUB_TOKEN = 'github_token'

# Used in Automated Outputs
VPC_ID = 'vpc_id'
AVAILABILITY_ZONE_1 = 'availability_zone_1'
AVAILABILITY_ZONE_2 = 'availability_zone_2'
AVAILABILITY_ZONE_3 = 'availability_zone_3'
SUBNET_ID_1 = 'subnet_id_1'
SUBNET_ID_2 = 'subnet_id_2'
SUBNET_ID_3 = 'subnet_id_3'
ROUTE_TABLE_1 = 'route_table_1'
ROUTE_TABLE_2 = 'route_table_2'
ROUTE_TABLE_3 = 'route_table_3'
SHARED_SECURITY_GROUP_ID = 'shared_security_group_id'
S3_KMS_KEY = 's3_kms_key'
S3_ACCESS_LOG_BUCKET = 's3_access_log_bucket'
S3_RAW_BUCKET = 's3_raw_bucket'
S3_CONFORMED_BUCKET = 's3_conformed_bucket'
S3_PURPOSE_BUILT_BUCKET = 's3_purpose_built_bucket'
CROSS_ACCOUNT_DYNAMODB_ROLE = 'cross_account_dynamodb_role'

GLUE_CONNECTION_AVAILABILITY_ZONE = 'glue_connection_availability_zone'
GLUE_CONNECTION_SUBNET = 'glue_connection_subnet'


def get_local_configuration(environment: str) -> dict:
    """
    Provides manually configured variables that are validated for quality and safety.
    @param: environment str: The environment used to retrieve corresponding configuration
    @raises: Exception: Throws an exception if the resource_name_prefix does not conform
    @raises: Exception: Throws an exception if the requested environment does not exist
    @return: dict:
    """
    local_mapping = {
        DEPLOYMENT: {
            ACCOUNT_ID: '634935009001',
            REGION: 'us-east-1',
            GITHUB_REPOSITORY_OWNER_NAME: 'paulomaiaribeiro',
            GITHUB_REPOSITORY_NAME: 'aws-cdk-pipelines-datalake-etl',
            # This is used in the Logical Id of CloudFormation resources.
            # We recommend Capital case for consistency.
            # Example: DataLakeCdkBlog
            LOGICAL_ID_PREFIX: 'DataLakeETL',
            # Important: This is used in resources that must be **globally** unique!
            # Resource names may only contain Alphanumeric and hyphens and cannot contain trailing hyphens.
            # Example: unique-identifier-data-lake
            RESOURCE_NAME_PREFIX: 'cdkdatalake',
        },
        DEV: {
            ACCOUNT_ID: '431274058968',
            REGION: 'us-east-1',
            VPC_CIDR: '10.20.0.0/24'
        },
        TEST: {
            ACCOUNT_ID: '595979353686',
            REGION: 'us-east-1',
            VPC_CIDR: '10.10.0.0/24'
        },
        PROD: {
            ACCOUNT_ID: '837323970389',
            REGION: 'us-east-1',
            VPC_CIDR: '10.0.0.0/24'
        }
    }

    resource_prefix = local_mapping[DEPLOYMENT][RESOURCE_NAME_PREFIX]
    if (
        not re.fullmatch('^[a-z|0-9|-]+', resource_prefix)
        or '-' in resource_prefix[-1:] or '-' in resource_prefix[1]
    ):
        raise Exception('Resource names may only contain lowercase Alphanumeric and hyphens '
                        'and cannot contain leading or trailing hyphens')

    if environment not in local_mapping:
        raise Exception(f'The requested environment: {environment} does not exist in local mappings')

    return local_mapping[environment]


def get_environment_configuration(environment: str) -> dict:
    """
    Provides all configuration values for the given target environment
    @param environment str: The environment used to retrieve corresponding configuration
    @return: dict:
    """
    cloudformation_output_mapping = {
        ENVIRONMENT: environment,
        VPC_ID: f'{environment}VpcId',
        AVAILABILITY_ZONE_1: f'{environment}AvailabilityZone1',
        AVAILABILITY_ZONE_2: f'{environment}AvailabilityZone2',
        AVAILABILITY_ZONE_3: f'{environment}AvailabilityZone3',
        SUBNET_ID_1: f'{environment}SubnetId1',
        SUBNET_ID_2: f'{environment}SubnetId2',
        SUBNET_ID_3: f'{environment}SubnetId3',
        ROUTE_TABLE_1: f'{environment}RouteTable1',
        ROUTE_TABLE_2: f'{environment}RouteTable2',
        ROUTE_TABLE_3: f'{environment}RouteTable3',
        SHARED_SECURITY_GROUP_ID: f'{environment}SharedSecurityGroupId',
        S3_KMS_KEY: f'{environment}S3KmsKeyArn',
        S3_ACCESS_LOG_BUCKET: f'{environment}S3AccessLogBucket',
        S3_RAW_BUCKET: f'{environment}RawBucketName',
        S3_CONFORMED_BUCKET: f'{environment}ConformedBucketName',
        S3_PURPOSE_BUILT_BUCKET: f'{environment}PurposeBuiltBucketName',
        CROSS_ACCOUNT_DYNAMODB_ROLE: f'{environment}CrossAccountDynamoDbRoleArn'
    }

    return {**cloudformation_output_mapping, **get_local_configuration(environment)}


def get_all_configurations() -> dict:
    """
    Returns a dict mapping of configurations for all environments.
    These keys correspond to static values, CloudFormation outputs, and Secrets Manager (passwords only) records.
    @return: dict:
    """
    return {
        DEPLOYMENT: {
            ENVIRONMENT: DEPLOYMENT,
            GITHUB_TOKEN: '/DataLake/GitHubToken',
            **get_local_configuration(DEPLOYMENT),
        },
        DEV: get_environment_configuration(DEV),
        TEST: get_environment_configuration(TEST),
        PROD: get_environment_configuration(PROD),
    }


def get_logical_id_prefix() -> str:
    """Returns the logical id prefix to apply to all CloudFormation resources
    @return: str:
    """
    return get_local_configuration(DEPLOYMENT)[LOGICAL_ID_PREFIX]


def get_resource_name_prefix() -> str:
    """Returns the resource name prefix to apply to all resources names
    @return: str:
    """
    return get_local_configuration(DEPLOYMENT)[RESOURCE_NAME_PREFIX]
