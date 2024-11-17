# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._keys_operations import build_create_if_not_exist_request, build_get_request, build_get_version_request, build_list_request, build_list_versions_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class KeysOperations:
    """KeysOperations async operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.keyvault.v2023_07_01.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    @distributed_trace_async
    async def create_if_not_exist(
        self,
        resource_group_name: str,
        vault_name: str,
        key_name: str,
        parameters: "_models.KeyCreateParameters",
        **kwargs: Any
    ) -> "_models.Key":
        """Creates the first version of a new key if it does not exist. If it already exists, then the
        existing key is returned without any write operations being performed. This API does not create
        subsequent versions, and does not update existing keys.

        :param resource_group_name: The name of the resource group which contains the specified key
         vault.
        :type resource_group_name: str
        :param vault_name: The name of the key vault which contains the key to be created.
        :type vault_name: str
        :param key_name: The name of the key to be created. The value you provide may be copied
         globally for the purpose of running the service. The value provided should not include
         personally identifiable or sensitive information.
        :type key_name: str
        :param parameters: The parameters used to create the specified key.
        :type parameters: ~azure.mgmt.keyvault.v2023_07_01.models.KeyCreateParameters
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Key, or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2023_07_01.models.Key
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Key"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-07-01")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(parameters, 'KeyCreateParameters')

        request = build_create_if_not_exist_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            key_name=key_name,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.create_if_not_exist.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Key', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_if_not_exist.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/keys/{keyName}"}  # type: ignore


    @distributed_trace_async
    async def get(
        self,
        resource_group_name: str,
        vault_name: str,
        key_name: str,
        **kwargs: Any
    ) -> "_models.Key":
        """Gets the current version of the specified key from the specified key vault.

        :param resource_group_name: The name of the resource group which contains the specified key
         vault.
        :type resource_group_name: str
        :param vault_name: The name of the vault which contains the key to be retrieved.
        :type vault_name: str
        :param key_name: The name of the key to be retrieved.
        :type key_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Key, or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2023_07_01.models.Key
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Key"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-07-01")  # type: str

        
        request = build_get_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            key_name=key_name,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Key', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/keys/{keyName}"}  # type: ignore


    @distributed_trace
    def list(
        self,
        resource_group_name: str,
        vault_name: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.KeyListResult"]:
        """Lists the keys in the specified key vault.

        :param resource_group_name: The name of the resource group which contains the specified key
         vault.
        :type resource_group_name: str
        :param vault_name: The name of the vault which contains the keys to be retrieved.
        :type vault_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either KeyListResult or the result of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.keyvault.v2023_07_01.models.KeyListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-07-01")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.KeyListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    vault_name=vault_name,
                    api_version=api_version,
                    template_url=self.list.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    vault_name=vault_name,
                    api_version=api_version,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("KeyListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/keys"}  # type: ignore

    @distributed_trace_async
    async def get_version(
        self,
        resource_group_name: str,
        vault_name: str,
        key_name: str,
        key_version: str,
        **kwargs: Any
    ) -> "_models.Key":
        """Gets the specified version of the specified key in the specified key vault.

        :param resource_group_name: The name of the resource group which contains the specified key
         vault.
        :type resource_group_name: str
        :param vault_name: The name of the vault which contains the key version to be retrieved.
        :type vault_name: str
        :param key_name: The name of the key version to be retrieved.
        :type key_name: str
        :param key_version: The version of the key to be retrieved.
        :type key_version: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Key, or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2023_07_01.models.Key
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Key"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2023-07-01")  # type: str

        
        request = build_get_version_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            key_name=key_name,
            key_version=key_version,
            api_version=api_version,
            template_url=self.get_version.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Key', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_version.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/keys/{keyName}/versions/{keyVersion}"}  # type: ignore


    @distributed_trace
    def list_versions(
        self,
        resource_group_name: str,
        vault_name: str,
        key_name: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.KeyListResult"]:
        """Lists the versions of the specified key in the specified key vault.

        :param resource_group_name: The name of the resource group which contains the specified key
         vault.
        :type resource_group_name: str
        :param vault_name: The name of the vault which contains the key versions to be retrieved.
        :type vault_name: str
        :param key_name: The name of the key versions to be retrieved.
        :type key_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either KeyListResult or the result of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.keyvault.v2023_07_01.models.KeyListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2023-07-01")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.KeyListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_versions_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    vault_name=vault_name,
                    key_name=key_name,
                    api_version=api_version,
                    template_url=self.list_versions.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_versions_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    vault_name=vault_name,
                    key_name=key_name,
                    api_version=api_version,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("KeyListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_versions.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/keys/{keyName}/versions"}  # type: ignore
