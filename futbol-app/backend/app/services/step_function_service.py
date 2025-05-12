import json
from typing import Dict, Type, Union

from botocore.client import BaseClient
from pydantic import BaseModel, ConfigDict


class StepFunctionService(BaseModel):
    function_arn: str
    input_model: Type[BaseModel]
    output_model: Type[BaseModel]
    client: BaseClient
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __get_input(self, payload: Union[BaseModel, Dict]):
        payload_dict = payload if isinstance(payload, Dict) else payload.dict()
        return self.input_model(**payload_dict).dict()

    def _invoke_function(
        self, payload: Union[BaseModel, Dict], sync_mode: bool = True
    ) -> BaseModel:
        input_payload = self.__get_input(payload)
        if sync_mode:
            output = json.loads(
                self.client.start_sync_execution(
                    stateMachineArn=self.function_arn, input=json.dumps(input_payload)
                ).get("output", "{}")
            )
            return self.output_model(**output)
        self.client.start_execution(
            stateMachineArn=self.function_arn, input=json.dumps(input_payload)
        )

    def invoke_async(self, payload: Union[BaseModel, Dict]):
        return self._invoke_function(payload, sync_mode=False)

    def invoke_sync(self, payload: Union[BaseModel, Dict]):
        return self._invoke_function(payload)
