# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import tempfile

import pytest

import biocommons.seqrepo.cli as srcli


@pytest.fixture
def opts():
    class MockOpts(object):
        pass

    test_dir = os.path.dirname(__file__)
    test_data_dir = os.path.join(test_dir, 'data')

    opts = MockOpts()
    opts.root_directory = os.path.join(tempfile.mkdtemp(prefix="seqrepo_pytest_"), "seqrepo")
    opts.fasta_files = [os.path.join(test_data_dir, "sequences.fa.gz")]
    opts.namespace = "test"
    opts.instance_name = str(datetime.date.today())
    opts.verbose = 0

    return opts


def test_init(opts):
    srcli.init(opts)
    assert os.path.exists(opts.root_directory)

    with pytest.raises(IOError) as excinfo:
        srcli.init(opts)

    seqrepo_dir = os.path.join(opts.root_directory, opts.instance_name)
    assert str(excinfo.value) == "{seqrepo_dir} exists and is not empty".format(seqrepo_dir=seqrepo_dir)


def test_load(opts):
    initial_namespace = opts.namespace
    with pytest.raises(RuntimeError) as excinfo:
        opts.namespace = "-"
        srcli.load(opts)
    assert str(excinfo.value) == "namespace == '-' is no longer supported"
    opts.namespace = initial_namespace

    srcli.load(opts)
    srcli.list_local_instances(opts)
    srcli.show_status(opts)
