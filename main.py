import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from globals import LANGCHAIN_API_KEY, apikey, GPT_MODEL, ambiguous_ds_en, interactive_app, advanced_logic, verbous

# useful tutorials:
# langchain OutputParser : https://www.youtube.com/watch?v=MlK6SIjcjE8&t=13s
# Pydantic: https://www.youtube.com/watch?v=R0RwdOc338w
# Pydantic+ langchain : https://www.youtube.com/watch?v=I4mFqyqFkxg

# =============================================================================
# part A external for streamlit and langchain etc
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langsmith import traceable

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY
st.set_page_config(layout="wide")
# =============================================================================
# Part B: internal
from create_templates import Create_Templates, AlertOutParser, Create_parsers, Load_Data_Streams

load_data_streams = Load_Data_Streams()
data_streams = load_data_streams.load_data_streams()


@traceable(name="Pipeline")
def run_main(user_query, verbous=False, interactive_app=False):
    # =============================================================================
    # define the LLM model
    os.environ['OPENAI_API_KEY'] = apikey
    llm = ChatOpenAI(model=GPT_MODEL, temperature=0)

    # =============================================================================
    # Prompt templates for ID dim mes etc
    create_templates = Create_Templates()
    ds_ID_template = create_templates.get_dsID_template()
    params_template = create_templates.get_params_template()

    # =============================================================================
    # Parser for ID dim mes etc
    create_parsers = Create_parsers()
    dsID_parser = create_parsers.get_dsID_parser()
    output_parser = AlertOutParser()

    # =============================================================================
    # for custom function
    load_data_streams = Load_Data_Streams()

    # =============================================================================
    # create chains
    ds_ID_chain = ds_ID_template | llm | dsID_parser
    #schema_chain = itemgetter("ds_ID") | RunnableLambda(load_data_streams.extruct_schema)
    #params_model_chain = itemgetter("schema") | RunnableLambda(create_parsers.get_params_model)

    def to_list(value):
        if not isinstance(value, list):
            return [value]
        return value


    # =============================================================================
    # run the LLM with the user's query
    if user_query:
        # find ds_ID
        all_long_output = []
        all_short_output = []
        ds_id = ds_ID_chain.invoke({'user_query': user_query})
        #print(ds_id)

        for ds, score in zip(to_list(ds_id.value), to_list(ds_id.probability)):
            # print (ds, score)
            # after we have the ds_ID we can dynamically define schema, parser

            schema = load_data_streams.data_streams[ds]         #new
            params_model = create_parsers.get_params_model(schema)                  #new
            params_parser = PydanticOutputParser(pydantic_object=params_model)
            format_instructions = create_templates.parser_to_massage(params_parser) # this is text

            # set params_chain. (since params_parser are define only after ds_ID is chosen, it must be here)
            params_chain = params_template | llm | params_parser
            params = params_chain.invoke({'user_query': user_query,
                                          'format_instructions': format_instructions,
                                          'schema': json.dumps(schema, indent=4), #create_templates.formate_json_to_text(schema),
                                          })

            # simplified_output
            if advanced_logic:
                long_output, short_output = output_parser.invoke(ds_ID=ds,
                                                                 params=params,
                                                                 id_is_ambiguous=ds_id.is_ambiguous,
                                                                 id_score=score)
            else:
                long_output, short_output = output_parser.invoke(ds_ID=ds,
                                                                 params=params)

            all_long_output.append(long_output)
            all_short_output.append(short_output)

        if interactive_app:
            if 'selected_option' not in st.session_state:
                st.session_state.selected_option = None

            final_alert = {}
            parameters_set = []
            scores = []
            for predicted_parameter_set in all_long_output:
                ds_id = predicted_parameter_set['ds_ID']
                alert_type = predicted_parameter_set['alert_type']
                alert_direction = predicted_parameter_set['alert_direction']
                alert_measures = predicted_parameter_set['alert_measure']
                alert_dimensions_list = predicted_parameter_set['alert_dimensions']
                alert_id_score = predicted_parameter_set['ambiguity_id_score']
                alert_measures_score = predicted_parameter_set['ambiguity_measure_score']
                alert_dimensions_score = predicted_parameter_set['ambiguity_dimensions_score']

                if isinstance(alert_dimensions_list[0], list):
                    # dimensions is a list of lists
                    for alert_measure,alert_measure_score in zip(alert_measures,alert_measures_score):
                        for alert_dimensions,alert_dimension_score in zip(alert_dimensions_list,alert_dimensions_score):
                            alert_score = alert_id_score*alert_measure_score*alert_dimension_score/(10*10*10)*100
                            parameters = {
                                'ds_ID': ds_id,
                                'alert_type': alert_type,
                                'alert_direction': alert_direction,
                                'alert_measure': alert_measure,
                                'alert_dimensions': alert_dimensions
                            }
                            parameters_set.append(parameters)
                            scores.append(alert_score)
                else:
                    # It's a single list
                    for alert_measure, alert_measure_score in zip(alert_measures, alert_measures_score):
                        alert_score = alert_id_score * alert_measure_score / (10 * 10) * 100
                        parameters = {
                            'ds_ID': ds_id,
                            'alert_type': alert_type,
                            'alert_direction': alert_direction,
                            'alert_measure': alert_measure,
                            'alert_dimensions': alert_dimensions_list
                        }
                        parameters_set.append(parameters)
                        scores.append(alert_score)
            predictions_num = len(parameters_set)
            if predictions_num > 1:
                st.write('There are several possible Alert Configurations that may satisfy your request: ')
                cols = st.columns(predictions_num)
                for i, col in enumerate(cols):
                    with col:
                        st.subheader(f"Configuration {i + 1}")
                        score = scores[i]
                        st.subheader(f" Relevancy {score:.0f}%")
                        st.write('Alert Configuration:', parameters_set[i])
                        if st.button(f"Select Option {i + 1}"):
                            st.session_state.selected_option = i + 1
                if st.session_state.selected_option is not None:
                    st.write(f"You selected Option {st.session_state.selected_option}")
                    selected_option = st.session_state.selected_option-1
                    final_alert = parameters_set[selected_option]
            else:
                final_alert = parameters_set[0]

            if final_alert:
                st.write(f"Alert Configuration:")
                st.write(final_alert)

        else:
            if verbous:
                print(f'params: {all_short_output}')

            return all_long_output


# =============================================================================
# Get user's query
if interactive_app:
    # Title of the app with a line break
    st.title("Anodot Alert Configuration Agent 🦜🔗\n")

    # Button to reset the input
    reset_button = st.button('Reset')
    # Handle the reset button click
    if reset_button:
        # Clear session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()  # Rerun the script to reset everything

    # Display the prompt with a line break using Markdown
    example1 = 'Alert me if food profit in Texas drops'
    example2 = 'I want to know about a significant decrease of users for advanced type'

    st.markdown(
        f"""
        <div style="font-family:Arial; font-size:16px; color:white;">
            <strong>Please add an alert request.</strong><br>            
            <span style="color:Green;">Example </span><br>
            <span style="color:Green;">{example1}</span><br>
        </div>
        """,
        unsafe_allow_html=True
    )

    load_data_streams = Load_Data_Streams()
    data_streams = load_data_streams.load_data_streams()
    for key in data_streams.keys():
        if st.sidebar.checkbox(f'Show Data Streams {key}'):
            st.sidebar.subheader(f'Data Streams {key}')
            st.sidebar.write(data_streams[key])

    user_query = st.text_input("")
    #user_query = 'Alert me if food profit drops'
    if user_query:
        run_main(user_query, interactive_app=interactive_app, verbous=verbous)
