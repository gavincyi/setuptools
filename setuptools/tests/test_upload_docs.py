import os
import shutil
import tempfile
import zipfile

import pytest

from setuptools.command.upload_docs import upload_docs
from setuptools.dist import Distribution

from .textwrap import DALS


SETUP_PY = DALS(
    """
    from setuptools import setup

    setup(name='foo')
    """)


@pytest.fixture
def sample_project(tmpdir_cwd):
    # setup.py
    with open('setup.py', 'wt') as f:
        f.write(SETUP_PY)

    os.mkdir('build')

    # A test document.
    with open('build/index.html', 'w') as f:
        f.write("Hello world.")

    # An empty folder.
    os.mkdir('build/empty')


@pytest.mark.usefixtures('sample_project')
@pytest.mark.usefixtures('user_override')
class TestUploadDocsTest:

    def test_create_zipfile(self):
        # Test to make sure zipfile creation handles common cases.
        # This explicitly includes a folder containing an empty folder.

        dist = Distribution()

        cmd = upload_docs(dist)
        cmd.target_dir = cmd.upload_dir = 'build'
        tmp_dir = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_dir, 'foo.zip')
        try:
            zip_file = cmd.create_zipfile(tmp_file)

            assert zipfile.is_zipfile(tmp_file)

            zip_file = zipfile.ZipFile(tmp_file) # woh...

            assert zip_file.namelist() == ['index.html']

            zip_file.close()
        finally:
            shutil.rmtree(tmp_dir)

