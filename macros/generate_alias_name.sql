{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- if custom_alias_name is none -%}
        {%- if target.name == 'prod' -%}
            {{ node.name }} 
        {%- elif target.name == 'staging-dev' -%}
            {{ node.name }} 
        {%- else -%}
            {{ target.schema }}_{{ target.name }}_{{ node.name }} 
        {%- endif -%}
    {%- else -%}    
        {{ custom_alias_name | trim }}
    {%- endif -%}
{%- endmacro %}
