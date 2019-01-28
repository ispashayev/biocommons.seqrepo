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
    opts.instance_name = "test"
    opts.verbose = 0

    opts.remote_host = "localhost"
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
    with pytest.raises(RuntimeError):
        opts.namespace = "-"
        srcli.load(opts)
    opts.namespace = initial_namespace

    opts.instance_name = str(datetime.date.today())
    srcli.load(opts)
    srcli.show_status(opts)  # TODO(@ispashayev): show_status not counting three sequences

    # print("=========")
    # print([fname for _, _, fnames in os.walk(os.path.join(opts.root_directory, opts.instance_name)) for fname in fnames])
    # print("STOP")
    # assert False


def test_list_instances(mocker, opts):
    srcli.load(opts)
    srcli.list_local_instances(opts)

    mocker.patch("biocommons.seqrepo.cli._get_remote_instances", new=srcli._get_local_instances)
    assert srcli._get_remote_instances(opts) == srcli._get_local_instances(opts)
    srcli.list_remote_instances(opts)
