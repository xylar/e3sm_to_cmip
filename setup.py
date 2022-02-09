import distutils.cmd
import os

from setuptools import find_packages, setup

from e3sm_to_cmip.version import __version__


class CleanCommand(distutils.cmd.Command):
    """
    Our custom command to clean out junk files.
    """
    description = "Cleans out junk files we don't want in the repo"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd_list = dict(
            DS_Store="find . -name .DS_Store -print0 | xargs -0 rm -f;",
            pyc="find . -name '*.pyc' -exec rm -rf {} \;",
            empty_dirs="find ./pages/ -type d -empty -delete;",
            build_dirs="find . -name build -print0 | xargs -0 rm -rf;",
            dist_dirs="find . -name dist -print0 | xargs -0 rm -rf;",
            egg_dirs="find . -name *.egg-info -print0 | xargs -0 rm -rf;"
        )
        for key, cmd in cmd_list.items():
            os.system(cmd)


setup(
    name="e3sm_to_cmip",
    version=__version__,
    author="Sterling Baldwin, Tom Vo, Chengzhu (Jill) Zhang, Anthony Bartoletti",
    author_email="vo13@llnl.gov, zhang40@llnl.gov",
    description="Transform E3SM model data output into cmip6 compatable data "
                "using the Climate Model Output Rewriter.",
    entry_points={'console_scripts':
                  ['e3sm_to_cmip = e3sm_to_cmip.__main__:main']},
    scripts=['e3sm_to_cmip/scripts/e2c_check_input_dataset.py',
             'e3sm_to_cmip/scripts/e2c_cmor-example.py',
             'e3sm_to_cmip/scripts/e2c_convert_land_variables.py',
             'e3sm_to_cmip/scripts/e2c_data_stager.py',
             'e3sm_to_cmip/scripts/e2c_esgf_check.py',
             'e3sm_to_cmip/scripts/e2c_find_sftlf_issue.py',
             'e3sm_to_cmip/scripts/e2c_fix_mask.py',
             'e3sm_to_cmip/scripts/e2c_fix_msftmz.py',
             'e3sm_to_cmip/scripts/e2c_fix_time.py',
             'e3sm_to_cmip/scripts/e2c_generate_xmls_cmip6.py',
             'e3sm_to_cmip/scripts/e2c_hash_dataset.py',
             'e3sm_to_cmip/scripts/e2c_join_output.py',
             'e3sm_to_cmip/scripts/e2c_output_checker.py',
             'e3sm_to_cmip/scripts/e2c_run_regrid.py',
             'e3sm_to_cmip/scripts/e2c_setup_cases.py',
             'e3sm_to_cmip/scripts/e2c_tar_to_bagit.py'],
    packages=['e3sm_to_cmip', 'e3sm_to_cmip.cmor_handlers'],
    package_dir={'e3sm_to_cmip': 'e3sm_to_cmip'},
    package_data={'e3sm_to_cmip': ['LICENSE'],
                  'e3sm_to_cmip.resources': ['*']},
    include_package_data=True,
    cmdclass={
        'clean': CleanCommand,
    })
