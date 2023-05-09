from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.05',
      description='Home_Work_GoIT',
      url='http://github.com/dummy_user/useful',
      author='Gennadiy Kirichenko',
      author_email='kirichenko.gennadiy@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)

