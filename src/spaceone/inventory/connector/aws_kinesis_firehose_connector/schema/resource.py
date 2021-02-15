from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_kinesis_firehose_connector.schema.data import DeliveryStreamDescription
from spaceone.inventory.libs.schema.dynamic_field import (
    TextDyField,
    DateTimeDyField,
)
from spaceone.inventory.libs.schema.dynamic_layout import (
    ItemDynamicLayout,
    TableDynamicLayout, ListDynamicLayout, )
from spaceone.inventory.libs.schema.resource import (
    CloudServiceResource,
    CloudServiceResponse,
    CloudServiceMeta,
)

"""
kinesis
"""
# TAB - Stream
firehose_meta_stream_details = ItemDynamicLayout.set_fields(
    "Stream Details",
    fields=[
        TextDyField.data_source("ARN", "data.delivery_stream_arn"),
        TextDyField.data_source("Status", "data.delivery_stream_status"),
        DateTimeDyField.data_source(
            "Data retention period", "data.create_timestamp"
        ),
        TextDyField.data_source("Permissions (IAM role)", "data.additional_tabs.iam_role"),
        TextDyField.data_source("CloudWatch error logging", "data.additional_tabs.cloud_watch_info"),
    ],
)

# TAB - Source
firehose_meta_source_details = ItemDynamicLayout.set_fields(
    "Source",
    fields=[
        TextDyField.data_source("Source", "data.source.source_details"),
        TextDyField.data_source("Server-side encryption for source records",
                                "data.delivery_stream_encryption_configuration.status"),
        TextDyField.data_source("Encryption type", "data.delivery_stream_encryption_configuration.key_type"),

    ]
)

# TAB - Transform source records with AWS Lambda
firehose_meta_lambda = ItemDynamicLayout.set_fields(
    "Transform source records with AWS Lambda",
    "data.additional_tabs.lambda_tab",
    fields=[
        TextDyField.data_source("Source record transformation", "source_record_transformation"),
        TextDyField.data_source("Lambda function", "lambda_func"),
        TextDyField.data_source("Lambda function version", "lambda_func_ver"),
        TextDyField.data_source("Timeout", "timeout"),
        TextDyField.data_source("Buffer conditions", "buffer_conditions")
    ]
)

# TAB - S3 backup
firehose_meta_s3_backup = ItemDynamicLayout.set_fields(
    "S3 backup",
    "data.additional_tabs.s3_backup_info",
    fields=[
        TextDyField.data_source("Backup mode", "backup_mode"),
        TextDyField.data_source("Backup S3 bucket", "bucket_name"),
        TextDyField.data_source("Backup S3 bucket error prefix", "bucket_error_prefix"),
        TextDyField.data_source("S3 buffer conditions", "buffer_conditions"),
        TextDyField.data_source("S3 compression", "compression"),
        TextDyField.data_source("S3 encryption", "encryption")
    ]
)

# TAB - S3 Destination
firehose_meta_s3_destination_details = ItemDynamicLayout.set_fields(
    "Amazon S3 Destination",
    "data.destinations.extended_s3_destination_description",
    fields=[
        TextDyField.data_source("S3 bucket", "bucket_name"),
        TextDyField.data_source("Prefix", "prefix"),
        TextDyField.data_source("Error prefix", "error_output_prefix"),
        TextDyField.data_source("Buffer conditions", "buffer_conditions"),
        TextDyField.data_source("Compression", "compression"),
        TextDyField.data_source("Encryption", "encryption_configuration.no_encryption")
    ]
)

firehose_meta_s3_destination_glue = ItemDynamicLayout.set_fields(
    "Convert record format",
    "data.destinations.extended_s3_destination_description.data_format_conversion_configuration",
    fields=[
        TextDyField.data_source("Record format conversion", "record_format_conversion"),
        TextDyField.data_source("Output format", "output_format"),
        TextDyField.data_source("Input format", "data.input_format"),
        TextDyField.data_source("AWS Glue region",
                                "schema_configuration.region"),
        TextDyField.data_source("AWS Glue database",
                                "schema_configuration.database_name"),
        TextDyField.data_source("AWS Glue table",
                                "schema_configuration.table_name"),
        TextDyField.data_source("AWS Glue table version",
                                "schema_configuration.version_id")
    ]
)

firehose_meta_s3_destination = ListDynamicLayout.set_layouts(
    "S3 Destination",
    layouts=[
        firehose_meta_s3_destination_details,
        firehose_meta_s3_destination_glue
    ],
)

# TAB - Http Endpoint Destination
firehose_meta_s3_destination_details = ItemDynamicLayout.set_fields(
    "Http Endpoint Destination",
    "data.destinations.http_endpoint_destination_description",
    fields=[
        TextDyField.data_source("HTTP endpoint name", "endpoint_configuration.name"),
        TextDyField.data_source("HTTP endpoint URL", "endpoint_configuration.url"),
        TextDyField.data_source("Content encoding", "request_configuration.content_encoding"),
        TextDyField.data_source("Retry duration", "retry_options.duration_in_seconds"),
        TextDyField.data_source("Buffer conditions", "buffer_conditions")
    ]
)

# TAB - Redshift Destination
firehose_meta_s3_destination_details = ItemDynamicLayout.set_fields(
    "Redshift Destination",
    "data.destinations.redshift_destination_description",
    fields=[
        TextDyField.data_source("COPY options", "copy_command.copy_options"),
        TextDyField.data_source("COPY command retry duration (seconds)", "retry_options.duration_in_seconds"),
        TextDyField.data_source("Cluster", "cluster"),
        TextDyField.data_source("User name", "username"),
        TextDyField.data_source("Database", "db_name"),
        TextDyField.data_source("Table", "copy_command.data_table_name"),
        TextDyField.data_source("Columns", "copy_command.data_table_columns")
    ]
)

# TAB - Tags
firehose_meta_tags = TableDynamicLayout.set_fields(
    "Tags",
    "data.tags",
    fields=[
        TextDyField.data_source("Key", "key"),
        TextDyField.data_source("Value", "value"),
    ],
)

# Overall
firehose_meta = CloudServiceMeta.set_layouts(
    [firehose_meta_stream_details,
     firehose_meta_source_details,
     firehose_meta_s3_backup,
     firehose_meta_lambda,
     firehose_meta_s3_destination,
     firehose_meta_tags]
)


class FirehoseResource(CloudServiceResource):  # service type - group
    cloud_service_group = StringType(default="KinesisDataFirehose")


class DeliveryStreamResource(FirehoseResource):  # service type - name
    cloud_service_type = StringType(default="DeliveryStream")
    data = ModelType(DeliveryStreamDescription)
    _metadata = ModelType(
        CloudServiceMeta, default=firehose_meta, serialized_name="metadata"
    )


class FirehoseResponse(CloudServiceResponse):
    resource = PolyModelType(DeliveryStreamResource)