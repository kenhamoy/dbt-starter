{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}_{{target.name}}
    {%- else -%}
        {%- if target.name == 'prod' -%}
            {{ custom_schema_name | trim }}      
        {%- elif target.name == 'staging-dev' -%}
            {{ custom_schema_name | trim }}    
        {%- else -%}             
            {{ custom_schema_name | trim }}_{{target.name}}  
        {%- endif -%}
    {%- endif -%}
{%- endmacro %}
