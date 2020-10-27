from io import StringIO
from contextlib import redirect_stdout

from mist.sdk import db, config, params

from .language_tools import get_mist_model, load_mist_language, \
    check_mist_parameters, check_installed_binaries


def execute():
    mist_model = get_mist_model()

    if config.simulate:
        print("[*] File loaded successfully")
    else:
        # Run user program!
        for c in mist_model.commands:
            c.launch()

def execute_from_text(text: str, fn_params: dict = None, **kwargs) -> str:
    if fn_params:
        params.update(fn_params)

    if kwargs:
        config.update(kwargs)

    # Set config defaults
    default_configs = {
        "console_output": True,
        "real_time": True,
        "debug": False,
        "persist": False,
        "database_path": None,
        "simulate": False,
        "no_check_tools": False
    }

    if need_config := set(default_configs.keys()).difference(kwargs.keys()):
        for c in need_config:
            config[c] = default_configs[c]

    mist_meta_model = load_mist_language(text)

    stream_stdout = StringIO()
    write_to_output = redirect_stdout(stream_stdout)

    with write_to_output:
        mist_model = mist_meta_model.model_from_str(text)

        # Check installed binaries
        check_installed_binaries(mist_model)

        # Check needed parameters for .mist
        check_mist_parameters(text)

        for c in mist_model.commands:
            c.launch()

    # Clean database
    db.clean_database()

    return stream_stdout.getvalue()

__all__ = ("execute", "execute_from_text")
