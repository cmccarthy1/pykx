import os
from pathlib import Path
from platform import system
import re
import shutil
import site
import subprocess
import sys

# Do not import pykx here - use the `kx` fixture instead!
import pytest


# Decorator for tests that may damage the environment they are run in, and thus should only be run
# in disposable environments such as within Docker containers in CI. GitLab Runners provides the
# env var we check for: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
disposable_env_only = pytest.mark.skipif(
    os.environ.get('CI_DISPOSABLE_ENVIRONMENT', '').lower() not in ('true', '1'),
    reason='Test must be run in a disposable environment',
)


@pytest.mark.unlicensed
def test_version(kx):
    assert re.fullmatch(r'(?:\d+\.){2}\d+.*', kx.__version__)


@pytest.mark.unlicensed
def test_dir(kx):
    assert isinstance(dir(kx), list)
    assert dir(kx) == sorted(dir(kx))


@pytest.mark.isolate
def test_qargs_q_flag():
    # PyKX used to fail on startup if the '-q' flag was manually provided
    os.environ['QARGS'] = '-q'
    import pykx as kx
    assert kx.q('2 + 2') == 4


@disposable_env_only
@pytest.mark.isolate
def test_QHOME_symlinks():
    # This logic to get QHOME is copied from `pykx.config`, since we can't use `pykx.qhome` until
    # after PyKX has been imported, but that would ruin the test.
    try:
        QHOME = Path(os.environ.get('QHOME', Path().home()/'q')).resolve(strict=True)
    except FileNotFoundError:
        # If QHOME and its fallback weren't set/valid, then q/Python must be
        # running in the same directory as q.k (and presumably other stuff one
        # would expect to find in QHOME).
        QHOME = Path().resolve(strict=True)
    p = QHOME/'extra.q'
    p.write_text('a:1b\n')

    q_lib_dir_name = {
        'Darwin': 'm64',
        'Linux': 'l64',
        'Windows': 'w64',
    }[system()]
    (QHOME/q_lib_dir_name).mkdir(exist_ok=True)
    fake_q_lib_path = Path(site.getsitepackages()[0])/'pykx'/'lib'/q_lib_dir_name/'fake_q_lib.so'
    fake_q_lib_path.touch()
    # Convert first argument of `shutil.move` to `str` to work around Python bug bpo-32689
    shutil.move(str(fake_q_lib_path), QHOME/q_lib_dir_name)

    assert not fake_q_lib_path.exists()
    import pykx as kx
    assert kx.q.extra.a # Ensure the q file in the user QHOME directory is available via symlink.
    assert fake_q_lib_path.exists()
    assert fake_q_lib_path.is_symlink()


def try_clean(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


@disposable_env_only
@pytest.mark.isolate
def test_QHOME_symlinks_skip():
    os.environ['IGNORE_QHOME'] = "1"
    # This logic to get QHOME is copied from `pykx.config`, since we can't use `pykx.qhome` until
    # after PyKX has been imported, but that would ruin the test.
    try:
        QHOME = Path(os.environ.get('QHOME', Path().home()/'q')).resolve(strict=True)
    except FileNotFoundError:
        # If QHOME and its fallback weren't set/valid, then q/Python must be
        # running in the same directory as q.k (and presumably other stuff one
        # would expect to find in QHOME).
        QHOME = Path().resolve(strict=True)
    p = QHOME/'skipped.q'
    p.write_text('a:1b\n')

    q_lib_dir_name = {
        'Darwin': 'm64',
        'Linux': 'l64',
        'Windows': 'w64',
    }[system()]
    (QHOME/q_lib_dir_name).mkdir(exist_ok=True)
    try_clean((QHOME/q_lib_dir_name/'fake_q_lib.so'))
    try_clean(Path(site.getsitepackages()[0])/'pykx'/'lib'/q_lib_dir_name/'fake_q_lib.so')
    fake_q_lib_path = Path(site.getsitepackages()[0])/'pykx'/'lib'/q_lib_dir_name/'fake_q_lib.so'
    fake_q_lib_path.touch()
    # Convert first argument of `shutil.move` to `str` to work around Python bug bpo-32689
    shutil.move(str(fake_q_lib_path), QHOME/q_lib_dir_name)
    try_clean(fake_q_lib_path)

    assert (QHOME/q_lib_dir_name).exists()
    assert (QHOME/'skipped.q').exists()
    assert not fake_q_lib_path.exists()
    import pykx as kx # noqa
    assert not fake_q_lib_path.exists()
    assert not (Path(site.getsitepackages()[0])/'pykx'/'skipped.q').exists()

    try_clean((QHOME/q_lib_dir_name/'fake_q_lib.so'))
    try_clean(fake_q_lib_path)


@pytest.mark.unlicensed
def test_top_level_attributes(kx):
    assert not set(dir(kx.exceptions)) - set(dir(kx))
    assert not set(dir(kx.wrappers)) - set(dir(kx))
    assert isinstance(kx.qhome, Path)
    assert isinstance(kx.qlic, Path)
    assert isinstance(kx.qargs, tuple)
    assert isinstance(kx.licensed, bool)
    assert isinstance(kx.q, kx.Q)
    assert isinstance(kx.q, kx.EmbeddedQ)
    assert issubclass(kx.EmbeddedQ, kx.Q)
    assert issubclass(kx.QConnection, kx.Q)


# TODO: Turn this text back on when the Q Lock timeout value is working again
# @pytest.mark.isolate
# def test_q_lock_error_timed():
#     import time
#
#     os.environ['PYKX_RELEASE_GIL'] = '1'
#     os.environ['PYKX_Q_LOCK'] = '3'
#
#     import pykx as kx
#
#     s = time.monotonic_ns()
#     with pytest.raises(kx.QError) as err:
#         kx.q('{[f] f peach til 20}', lambda x: kx.q(f'til {x}'))
#         assert 'Attempted to acquire lock on already locked call into q.' in str(err.value)
#     e = time.monotonic_ns()
#     run_time = (e - s) * 0.000000001 # convert time back to seconds
#     assert run_time > 3.0 and run_time < 4.0


@pytest.mark.isolate
def test_q_lock_error_instant():
    os.environ['PYKX_RELEASE_GIL'] = '1'
    os.environ['PYKX_Q_LOCK'] = '0'

    import pykx as kx

    with pytest.raises(kx.QError) as err:
        kx.q('{[f] f peach til 20}', lambda x: kx.q(f'til {x}'))
        assert 'Attempted to acquire lock on already locked call into q.' in str(err.value)


@pytest.mark.isolate
def test_pykx_safe_reimport():
    import pykx as kx
    with kx.PyKXReimport():
        output = subprocess.run(
            (str(Path(sys.executable).as_posix()), '-c', 'import pykx; print(pykx.q("til 10"))'),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ).stdout.strip()
        assert output == "0 1 2 3 4 5 6 7 8 9"
