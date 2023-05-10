import os
import subprocess
import shutil
from rich import print
from setuptools.command.build_py import build_py
from setuptools import setup

about = {}
root_path = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(root_path, "reatool", "__version__.py")
with open(version_path, "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


class BuildCommand(build_py):
    def run(self):
        dist_path = os.path.join(root_path, "dist")
        assert_path = os.path.join(root_path, "asserts")
        dist_assert_path = os.path.join(dist_path, "asserts")
        target_path = os.path.join(root_path, "target")
        build_path = os.path.join(root_path, "build")

        print("[bold]:broom: Clear target folder")
        shutil.rmtree(target_path, ignore_errors=True)
        shutil.rmtree(dist_path, ignore_errors=True)
        shutil.rmtree(build_path, ignore_errors=True)

        print("[bold]:file_folder: Copy assets to dist")
        aria2c_name = "aria2c.exe"
        aria2c_html_name = "aria2c.html"
        shutil.copytree(assert_path, dist_assert_path)
        shutil.copyfile(os.path.join(root_path, aria2c_name), os.path.join(dist_path, aria2c_name))
        shutil.copyfile(os.path.join(root_path, aria2c_html_name), os.path.join(dist_path, aria2c_html_name))
        os.makedirs(target_path, exist_ok=True)

        print("[bold]:building_construction: Build the application by Pyinstaller")
        logo_path = os.path.join(assert_path, "logo.ico")
        subprocess.run(['pyinstaller', '-F', '-i', logo_path, '-w', '-n', "ReaTool", "main.py"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("[bold]:broom: Clear build, dist folder")
        shutil.rmtree(build_path, ignore_errors=True)
        shutil.rmtree(f"{about['__title__']}.egg-info", ignore_errors=True)
        os.remove(f"{about['__title__']}.spec")

        print("[bold]:package: Create a ZIP archive of the disk contents")
        zip_filename = f"{about['__title__']}v{about['__version__']}"
        archive_name = shutil.make_archive(os.path.join(target_path, zip_filename), "zip", dist_path)
        print(f"[bold]:tada: Build success, location is: {archive_name}")


# Configure the package metadata and dependencies
setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    keywords="tool xhs crawl",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    packages=["reatool"],
    install_requires=[
        'pyinstaller',
        'PySide6',
        'requests',
        'segno',
        'xhs',
        'browser-cookie3',
        'rich',
    ],
    cmdclass={
        'build_py': BuildCommand,
    }
)
