import io
import os
import subprocess
import sys

import nbformat
import numpy as np
import pytest
from test_r import r_installed


# taken from the execellent example here:
# https://blog.thedataincubator.com/2016/06/testing-jupyter-notebooks/

def _notebook_run(nb_path, tmp_path, env=os.environ, kernel=None):
    """Execute a Jupyter notebook via nbconvert and collect output.

    Parameters
    ----------
    nb_path : path-like
        The notebook file to execute.
    tmp_path : path-like
        A directory in which to create temporary output.
    env : dict-like
        Execution environment for `nbconvert`.
    kernel : str
        Jupyter kernel to use. Default: `python2` or `python3`, matching the
        current Python version.

    Returns
    -------
    nb : :class:`nbformat.NotebookNode`
        Parsed and executed notebook.
    errors : list
        Any execution errors.
    """
    major_version = sys.version_info[0]
    kernel = kernel or 'python{}'.format(major_version)
    # str() here is for python2 compatibility
    os.chdir(str(nb_path.parent))
    fname = tmp_path / 'test.ipynb'
    args = [
        "jupyter", "nbconvert", "--to", "notebook", "--execute",
        "--ExecutePreprocessor.timeout=60",
        "--ExecutePreprocessor.kernel_name={}".format(kernel),
        "--output", str(fname), str(nb_path)]
    subprocess.check_call(args, env=env)

    # str() here is for python2 compatibility
    nb = nbformat.read(io.open(str(fname), encoding='utf-8'),
                       nbformat.current_nbformat)

    errors = [
        output for cell in nb.cells if "outputs" in cell
        for output in cell["outputs"] if output.output_type == "error"
    ]

    fname.unlink()

    return nb, errors


def test_py_transport(tutorial_path, tmp_path, tmp_env):
    fname = tutorial_path / 'transport' / 'py_transport.ipynb'
    nb, errors = _notebook_run(fname, tmp_path, tmp_env)
    assert errors == []

    obs = eval(nb.cells[-5]['outputs'][0]['data']['text/plain'])['lvl']
    exp = 153.6750030517578
    assert np.isclose(obs, exp)


def test_py_transport_scenario(tutorial_path, tmp_path, tmp_env):
    fname = tutorial_path / 'transport' / 'py_transport_scenario.ipynb'
    nb, errors = _notebook_run(fname, tmp_path, tmp_env)
    assert errors == []

    obs = eval(nb.cells[-9]['outputs'][0]['data']['text/plain'])['lvl']
    exp = 153.6750030517578
    assert np.isclose(obs, exp)

    obs = eval(nb.cells[-8]['outputs'][0]['data']['text/plain'])['lvl']
    exp = 161.3249969482422
    assert np.isclose(obs, exp)


@pytest.mark.skipif(not r_installed(), reason='requires R to be installed')
def test_R_transport(tutorial_path, tmp_path, tmp_env):
    fname = tutorial_path / 'transport' / 'R_transport_ret.ipynb'
    nb, errors = _notebook_run(fname, tmp_path, tmp_env, kernel='IR')
    assert errors == []


@pytest.mark.skipif(not r_installed(), reason='requires R to be installed')
def test_R_transport_scenario(tutorial_path, tmp_path, tmp_env):
    fname = tutorial_path / 'transport' / 'R_transport_scenario_ret.ipynb'
    nb, errors = _notebook_run(fname, tmp_path, tmp_env, kernel='IR')
    assert errors == []
