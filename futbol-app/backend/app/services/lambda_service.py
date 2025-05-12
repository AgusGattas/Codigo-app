import json
from typing import Dict, Type, Union

from botocore.client import BaseClient
from pydantic import BaseModel, ConfigDict


class LambdaService(BaseModel):
    function_name: str
    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    client: BaseClient
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _invoke_lambda(
        self, payload: Union[BaseModel, Dict], mode: str = "RequestResponse"
    ) -> BaseModel:
        input_body = self.__get_input(payload)
        payload = bytes(json.dumps(input_body), encoding="utf8")
        return self.output_model(
            **json.loads(
                self.client.invoke(
                    FunctionName=self.function_name,
                    InvocationType=mode,
                    Payload=payload,
                )["Payload"].read()
                or "{}"
            )
        )

    def __get_input(self, payload: Union[BaseModel, Dict]):
        payload_dict = payload if isinstance(payload, Dict) else payload.dict()
        return self.input_model(**payload_dict).dict()

    def invoke_async(self, payload):
        return self._invoke_lambda(payload, mode="Event")

    def invoke_sync(self, payload):
        return self._invoke_lambda(payload)
