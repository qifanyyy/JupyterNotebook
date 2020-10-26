import ibm_boto3
import ibm_botocore

class COSBackend:
    """
    A wrap-up around COS imb_boto3 APIs.
    """

    def __init__(self, cos_config):
        service_endpoint = cos_config.get('endpoint').replace('http', 'https:')
        secret_key = cos_config.get('secret_key')
        access_key = cos_config.get('access_key')
        client_config = ibm_botocore.client.Config(max_pool_connections=200, user_agent_extra='pywren-ibm-cloud')
        self.cos_client = ibm_boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, config=client_config, endpoint_url=service_endpoint)


    def put_object(self, bucket_name, key, data):
        """
        Put an object in COS. Override the object if the key already exists.
        :param key: key of the object
        :param data: data of the object
        :type data: str/bytes
        :return: None
        """
        try:
            res = self.cos_client.put_object(Bucket=bucket_name, Key=key, Body=data)
            status = 'OK' if res['ResponseMetadata']['HTTPStatusCode'] == 200 else 'Error'
            try:
                print ('PUT Object {} - Size: {} - {}'.format(key, sizeof_fmt(len(data)), status))
            except:
                print ('PUT Object {} {}'.format(key, status))
        except ibm_botocore.exceptions.ClientError as e:
            raise e


    def get_object(self, bucket_name, key, stream=False, extra_get_args={}):
        """
        Get object from COS with a key. Throws StorageNoSuchKeyError if the given key does not exist.
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """

        try:
            r = self.cos_client.get_object(Bucket=bucket_name, Key=key, **extra_get_args)
            if stream:
                data = r['Body']
            else:
                data = r['Body'].read()
            return data
        except ibm_botocore.exceptions.ClientError as e:
            raise e


    def head_object(self, bucket_name, key):
        """
        Head object from COS with a key. Throws StorageNoSuchKeyError if the given key does not exist
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """
        try:
            metadata = self.cos_client.head_object(Bucket=bucket_name, Key=key)
            return metadata['ResponseMetadata']['HTTOHeaders']
        except ibm_botocore.exceptions.ClientError as e:
            raise e


    def delete_object(self, bucket_name, key):
        """
        Delete an object form storage.
        :param bucket: bucket name
        :param key: data key
        """
        return self.cos_client.delete_object(Bucket=bucket_name, Key=key)


    def list_objects(self, bucket_name, prefix=None):
        paginator = self.cos_client.get_paginator('list_objects_v2')
        try:
            if (prefix is not None):
                page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            else:
                page_iterator = paginator.paginate(Bucket=bucket_name)

            object_list = []
            for page in page_iterator:
                if 'Contents' in page:
                    for item in page['Contents']:
                        object_list.append(item)
            return object_list
        except ibm_botocore.exceptions.ClientError as e:
            raise e

