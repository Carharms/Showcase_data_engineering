import inspect
from rich.table import Table
from rich.console import Console


def clean_dict(dct):
    """
    Implement via a single dictionary compehension
    that returns a dictionary without the keys that
    start with "_".

    Parameters: `dct` - A dictionary.

    Returns: A new dictionary with all non-underscore-prefixed items.
    """
    # removes key: value pairs for items without a "_" at index[0]
    dct_comprhension = {key: value for key, value in dct.items() if not key[0] == "_"}
    return dct_comprhension


def find_conflicts(local_vars):
    """
    Return a dictionary that shows you the scope of the current function.

    Parameters:

    local_vars: a dictionary of locals obtained from the parent scope

    Returns:

    Dictionary with 2 keys:

    "locals": all local variables, but without underscore keys

    "conflicts": a dictionary of all items that are in `local_vars` and also in `globals()`
                 excluding underscore keys
    """

    # create dictionaries for local and global variables
    updated_locals = clean_dict(local_vars)
    updated_globals = clean_dict(globals())

    conflicts = {}

    # cross reference dictionaries to determine if conflicting keys
    for key in updated_locals:
        if key in updated_globals:
            # add identical variables in the dictionaries to the conflicts dictionary
            conflicts[key] = updated_globals[key]

    final_dict = {"locals": updated_locals, "conflicts": conflicts}
    return final_dict


def sc():
    """
    This is the intended interface for scope_check, a user would

    from scope_check import sc

    And then where they have questions about scope, can simply call sc()
    to see what is happening.
    """

    # this is advanced/unique code to get the parent frame
    # allowing access to the parent function's state/locals
    # you would not do this in a typical python program
    # but it is useful for writing tools that interact with
    # python itself like a debugger or our helper function here
    frame = inspect.currentframe()
    try:
        locs = frame.f_back.f_locals
        filename = frame.f_back.f_code.co_filename
        line_num = frame.f_back.f_lineno
    finally:
        del frame

    scope = find_conflicts(locs)

    # this code builds a `rich.Table` for nice looking output
    table = Table(title=f"{filename.split('/')[-1]} line {line_num}")
    table.add_column("name", style="cyan", width=20)
    table.add_column("value", overflow="ellipsis", width=30, no_wrap=True)
    table.add_column("type", width=10)
    table.add_column("global?", style="red", width=30, no_wrap=True)
    for k, v in scope["locals"].items():
        if k in scope["conflicts"]:
            global_val = scope["conflicts"][k]
        else:
            global_val = ""
        table.add_row(
            k,
            str(v),
            type(v).__name__,
            str(global_val),
            style="red" if global_val else None,
        )
    Console().print(table)


x = "global x is a string"

if __name__ == "__main__":

    def test_function(a, b):
        x = 3
        y = 4
        z = "this is a long string" * 100  # noqa
        sc()
        return x + y

    test_function(1, 2)
