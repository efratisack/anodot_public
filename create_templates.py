# =============================================================================
# Add the parent directory to sys.path
import os
import json

# =============================================================================
# part A for streamlit and langchain
#from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate,HumanMessagePromptTemplate, SystemMessagePromptTemplate

# =============================================================================
# part B for pydentic
#from langchain.output_parsers import PydanticOutputParser
#from pydantic import BaseModel, Field, create_model
from typing import List, Literal, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, create_model, Field, conlist, confloat,conint
from globals import data_path, datastreams_file_name, advanced_logic

# =============================================================================
# Part C: internal
from synthetic_data_creation.create_synthetic_data import load_synthetic_data_streams
from all_prompts import all_prompts

class Load_Data_Streams():
    def __init__(self):
        file_path = os.path.join(data_path, datastreams_file_name)
        self.data_streams = load_synthetic_data_streams(file_path)

    def load_data_streams(self):
        return self.data_streams

    def extruct_schema(self,ds_ID):
        schema = self.data_streams[ds_ID]
        #sample_txt = json.dumps(schema['sample'], indent=2)
        return schema

class Create_Templates():
    def __init__(self):
        lds = Load_Data_Streams()
        self.data_streams = lds.load_data_streams()
        self.create_parsers = Create_parsers()

    def formate_json_to_text(self,txt):
        txt_str = str(txt)
        formatted_txt_str = txt_str.replace('{', '(').replace('}', ')')
        return formatted_txt_str

    def parser_to_massage(self, pydantic_parser) -> object:
        #create instructions for prompt based on pydantic_parser but without the foo bar example
        format_instructions = pydantic_parser.get_format_instructions()
        instructions = all_prompts['customized_pydentic'] + format_instructions.split("Here is the output schema:")[1]
        return instructions

    def get_dsID_template(self):
        # define parser
        pydantic_parser = self.create_parsers.get_dsID_parser()
        format_instructions = self.parser_to_massage(pydantic_parser)  # this will used for the prompt input
        # define messages
        system_message_format = SystemMessagePromptTemplate.from_template("Please provide ds ID based on the following format instructions:\n{format_instructions}")
        system_message = all_prompts['system_prompt_ds_ID'] + self.formate_json_to_text(self.data_streams)
        human_message = HumanMessagePromptTemplate.from_template("{user_query}")
        # define template
        template = ChatPromptTemplate.from_messages([system_message, system_message_format, human_message])
        template = template.partial(format_instructions=format_instructions)
        return template

    def get_params_template(self):
        # define messages
        system_message_format = SystemMessagePromptTemplate.from_template("use format instructions:\n{format_instructions}")
        system_message = all_prompts['general_system_prompt'] + '\nData Stream Schema: {schema}' #+ '\nDimensions Sample: {sample}'
        human_message = HumanMessagePromptTemplate.from_template("{user_query}")
        # define template
        template = ChatPromptTemplate.from_messages([system_message, system_message_format, human_message])
        return template

class Create_parsers():
    def __init__(self):
        lds = Load_Data_Streams()
        self.data_streams = lds.load_data_streams()

    def get_dsID_parser(self):
        # define pydantic_parser
        data_streams = self.data_streams
        if advanced_logic:
            ds_id_model = self.create_literal_pydantic_model_with_prob(data_streams.keys(), all_prompts["pyd_description_ds_ID"], all_prompts["pyd_instruction_ds_ID"])
        else:
            ds_id_model = self.create_literal_pydantic_model(data_streams.keys(), all_prompts["pyd_description_ds_ID"], all_prompts["pyd_instruction_ds_ID"])
        pydantic_parser = PydanticOutputParser(pydantic_object=ds_id_model)
        return pydantic_parser

    def get_params_model(self,data_stream_schema):
        #dimensions_txt = "the dimensions should be only from this list: dimensions:" + str(data_stream_schema['dimensions'])
        #sample_txt = "full context:" + str(data_stream_schema['sample'])

        # define pydantic_parser
        class SearchExpressionModel(BaseModel):
            alert_type:         self.get_type_model()
            alert_direction:    self.get_direction_model()
            alert_measure:      self.get_measure_model(data_stream_schema['measures'], all_prompts["pyd_description_measure"], all_prompts["pyd_instruction_measure"])
            alert_dimensions:   self.get_dimension_model(data_stream_schema['dimensions'], all_prompts["pyd_description_dimensions"], all_prompts["pyd_instruction_dimensions"])# + dimensions_txt + sample_txt)
            alert_title:        self.get_title_model()

        return SearchExpressionModel

    def get_measure_model(self, keys, description, instruction):
        if advanced_logic:
            model = self.create_literal_pydantic_model_with_prob(keys, description, instruction)
        else:
            model = self.create_literal_pydantic_model(keys, description, instruction)
        return model

    def get_dimension_model(self, keys, description, instruction):
        if advanced_logic:
            model = self.create_dimension_pydantic_model_with_prob(keys, description, instruction)
        else:
            model = self.create_list_pydantic_model(keys, description, instruction)
        return model

    def get_direction_model(self):
        class AlertDirectionModel(BaseModel):
            value: Literal['up', 'down', 'both'] = Field(description=all_prompts["pyd_description_direction"])
        return AlertDirectionModel

    def get_type_model(self):
        class AlertTypeModel(BaseModel):
            value: Literal['anomaly', 'static', 'no data'] = Field(default='anomaly', description=all_prompts["pyd_description_type"])
        return AlertTypeModel

    def get_title_model(self):
        class AlertTitleModel(BaseModel):
            value: str = Field(description=all_prompts['pyd_description_title'])
        return AlertTitleModel

    def create_literal_pydantic_model(self, values, description, instruction):
        values_to_create = Literal[tuple(values)]
        literal_model = create_model(
            'FixedListModel',
            value=(values_to_create, Field(..., description=f"{description} ' ' {instruction}")),
            probability=(float, Field(default=10, description="Fixed probability score of 10"))
        )
        return literal_model


    def create_literal_pydantic_model_with_prob(self, values, description, instruction):
        #values_to_create = List[Literal[tuple(values)]]
        literal_model = create_model(
            'FixedListModel',
            value=(conlist(Literal[tuple(values)], min_length=1, max_length=2), Field(..., description=f"{description}. {instruction}")),
            #value=(values_to_create, Field(..., description=f"{description} ' ' {instruction}")),
            is_ambiguous=(bool, Field(default=0, description=all_prompts["pyd_description_ambiguous"])),
            probability=(List[conint(ge=0, le=10)], Field(...)),
            explanation=(str, Field(...,
            description="Explanation of the how values were selected"))
        )
        return literal_model

    def create_dimension_pydantic_model_with_prob(self, values, description, instruction):
        literal_model = create_model(
            'DimensionsModel',
            value=(conlist(Literal[tuple(values)], min_length=1), Field(..., description=f"{description}. {instruction}")),
            #value=(values_to_create, Field(..., description=f"{description} ' ' {instruction}")),
            is_ambiguous=(bool, Field(default=0, description=all_prompts["pyd_description_ambiguous"])),
            probability=(List[conint(ge=0, le=10)], Field(...)),
            explanation=(str, Field(..., description="Explanation of the how dimensions were selected"))
        )
        return literal_model

    def create_list_pydantic_model(self, values, description: str, instruction: str):
        values_literal = Literal[tuple(values)]
        field_type = List[values_literal]

        literal_model = create_model(
            'FixedListModel',
            value=(field_type, Field(..., description=f"{description} {instruction}")),
            probability=(float, Field(default=10, description="Fixed probability score of 10"))
        )
        return literal_model

class AlertOutParser:
    def __init__(self, ):
        pass

    def invoke(self,ds_ID, params, id_is_ambiguous=None, id_score=None):
        if params.alert_type.value == 'no data':
            params.alert_direction.value = 'both'
        if advanced_logic:
            long_output = {
                "ds_ID": ds_ID,
                "alert_type": params.alert_type.value,
                "alert_direction": params.alert_direction.value,
                "alert_measure": params.alert_measure.value,
                "measure_reasoning": params.alert_measure.explanation,
                "alert_dimensions": params.alert_dimensions.value,
                "dimensions_reasoning": params.alert_dimensions.explanation,
                "alert_title": params.alert_title.value,
                "ambiguity_id": id_is_ambiguous,
                "ambiguity_id_score": id_score,
                "ambiguity_measure": params.alert_measure.is_ambiguous,
                "ambiguity_measure_score": params.alert_measure.probability,
                "ambiguity_dimensions": params.alert_dimensions.is_ambiguous,
                "ambiguity_dimensions_score": params.alert_dimensions.probability,
            }
        else:
            long_output = {
                "ds_ID": ds_ID,
                "alert_type": params.alert_type.value,
                "alert_direction": params.alert_direction.value,
                "alert_measure": params.alert_measure.value,
                "alert_dimensions": params.alert_dimensions.value,
                "alert_title": params.alert_title.value,
            }
        short_output = {
            "data_stream_ID": long_output["ds_ID"],
            "measure": long_output["alert_measure"],
            "dimensions": long_output["alert_dimensions"]
        }
        return long_output, short_output

    #def __repr__(self) -> str:
    #    return str(self.invoke())

