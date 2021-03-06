import platform
from conan.packager import ConanMultiPackager, os, re


def get_name_version_from_recipe():
    with open("conanfile.py", "r") as conanfile:
        contents = conanfile.read()
        name = re.search(r'name\s*=\s*"(\S*)"', contents).groups()[0]
        version = re.search(r'version\s*=\s*"(\S*)"', contents).groups()[0]
    return name, version

def get_default_vars():
    username = os.getenv("CONAN_USERNAME", "bincrafters")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    _, version = get_name_version_from_recipe()
    return username, channel, version

def is_ci_running():
    return os.getenv("APPVEYOR_REPO_NAME","") or os.getenv("TRAVIS_REPO_SLUG","")

def get_ci_vars():
    reponame_a = os.getenv("APPVEYOR_REPO_NAME","")
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH","")

    reponame_t = os.getenv("TRAVIS_REPO_SLUG","")
    repobranch_t = os.getenv("TRAVIS_BRANCH","")

    username, _ = reponame_a.split("/") if reponame_a else reponame_t.split("/")
    channel, version = repobranch_a.split("/") if repobranch_a else repobranch_t.split("/")
    return username, channel, version

def get_env_vars():
    return get_ci_vars() if is_ci_running() else get_default_vars()

if __name__ == "__main__":
    name, _ = get_name_version_from_recipe()
    username, channel, version = get_env_vars()
    reference = "{0}/{1}".format(name, version)
    upload = "https://api.bintray.com/conan/{0}/public-conan".format(username)

    builder = ConanMultiPackager(username=username, channel=channel, reference=reference, upload=upload,
                                 upload_only_when_stable=True, stable_branch_pattern="stable/*")
    builder.add_common_builds(shared_option_name="%s:shared" % name, pure_c=False)

    # Header only
    if platform.system() == "Linux" and os.getenv("CONAN_GCC_VERSIONS", False) == "6.3":
        builder.add({}, {"%s:header_only" % name: True}, {}, {})

    builder.run()
