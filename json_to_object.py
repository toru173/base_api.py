# Copyright (c) 2024-present toru173 and contributors
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted (subject to the limitations in the disclaimer 
# below) provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of the contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY 
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Union, Optional, Any
from types import SimpleNamespace

import json
import re

def json_to_object(data: Union[dict, str], use_snake_case: Optional[bool] = False) -> SimpleNamespace:
    """
    Recursively converts a JSON string or dict into nested Python objects.
    Top-level must be a dict.

    - Dicts become SimpleNamespace objects with keys as attributes.
    - Lists remain Python lists, with their elements recursively converted.
    - Primitives (str, int, float, bool, None) remain unchanged.
    
    If use_snake_case = True, JSON keys in camelCase are converted to snake_case.
    
    :param data: A JSON string or a dictionary.
    :param use_snake_case: Whether to convert keys to snake_case.
    :return: A SimpleNamespace representing the top-level JSON object.
    :raises TypeError: If input is not a string or dictionary.
    :raises ValueError: If the string cannot be parsed as a top-level JSON object.
    """

    if not isinstance(data, (str, dict)):
        raise TypeError(f"Invalid type. Expected str or dict, but got a {type(data)}")
    
    if isinstance(data, str):
        try:
            data = json.loads(data)
            if not isinstance(data, dict):
                raise ValueError(f"Expected a top-level JSON object (dict), but got a {type(data)}")
        except json.JSONDecodeError as e:
            raise

    def _camel_to_snake(name: str) -> str:
        # Insert underscores before uppercase letters (not at start), then convert to lowercase
        s = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return s        

    def _json_to_object(data: Any) -> Any:

        if isinstance(data, dict):
            namespace = SimpleNamespace()
            for key, value in data.items():
                if use_snake_case:
                    key = _camel_to_snake(key)
                setattr(namespace, key, _json_to_object(value))
            return namespace
        
        elif isinstance(data, list):
            return [_json_to_object(elem) for elem in data]
        
        else:
            return data
    
    return _json_to_object(data)
