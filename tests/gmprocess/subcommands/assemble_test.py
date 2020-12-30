#!/usr/bin/env python
import io
import os
import shutil
import pkg_resources


def test_assemble(script_runner):
    try:
        # Need to create profile first.
        cdir = 'pytest_gmp_proj_dir'
        ddir = pkg_resources.resource_filename(
            'gmprocess', os.path.join('data', 'testdata', 'demo'))
        setup_inputs = io.StringIO(
            "test\n%s\n%s\nname\nemail\n" % (cdir, ddir)
        )
        ret = script_runner.run('gmp', 'projects', '-c', stdin=setup_inputs)
        assert ret.success

        ret = script_runner.run('gmp', 'assemble', '-h')
        assert ret.success

        ret = script_runner.run('gmp', 'assemble')
        assert ret.success

        ret = script_runner.run('gmp', 'assemble', '-e', 'ci38457511', '-o')
        assert ret.success

        external_source = pkg_resources.resource_filename(
            'gmprocess', os.path.join('data', 'testdata', 'demo2'))
        ret = script_runner.run(
            'gmp', 'assemble', '-e', 'usp000a1b0', '-d', external_source)
        assert ret.success

    except Exception as ex:
        raise ex
    finally:
        shutil.rmtree('pytest_gmp_proj_dir')
        # Remove workspace and image files
        pattern = ['workspace.h5', '.png']
        for root, _, files in os.walk(ddir):
            for file in files:
                if any(file.endswith(ext) for ext in pattern):
                    os.remove(os.path.join(root, file))


if __name__ == '__main__':
    test_assemble()
