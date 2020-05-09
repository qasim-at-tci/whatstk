import os
import json


this_directory = os.path.abspath(os.path.dirname(__file__))
assets_folder = 'assets'
hformat_support_filename = 'header_format_support.json'
hformat_support_filepath = os.path.join(this_directory, assets_folder, hformat_support_filename)


def is_supported(hformat):
    """Check if header `hformat` is currently supported.

    Args:
        hformat (str): Header format.

    Returns:
        tuple: 
            - bool: True if header is supported.
            - bool: True if header is supported with `auto_header` feature.

    """
    with open(hformat_support_filepath, 'r') as f:
        h = json.load(f)

    if ('%P' in hformat or "%p" in hformat):
        hformat = hformat.replace("%P", "%p").replace("%H", "%I")
    if '%y' in hformat:
        hformat.replace('%y', '%Y')
    auto_header_support = 0
    support = 0
    for hh in h:
        if hformat == hh['format'] :
            support = 1
            auto_header_support = hh['auto_header']
    
    return bool(support), bool(auto_header_support)

def is_supported_verbose(hformat):
    """Check if header `hformat` is currently supported, manually and using `auto_header`.

    Result is shown as a string.

    Args:
        hformat (str): Information message.

    """
    support, auto_header_support = is_supported(hformat)

    msg = "The header '{}' is {}supported. `auto_header` for this header is {}supported.".format(
        hformat,
        'not ' if not support else '',
        'not ' if not auto_header_support else '',
    )
    return msg


def get_list_supported_hformats():
    """Get list of supported formats.

    Returns:
        list: List with supported formats (as str).

    """
    with open(hformat_support_filepath, 'r') as f:
        h = json.load(f)
    return [hh['format'] for hh in h]