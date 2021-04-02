import gitlab
import argparse
import semver

def generate_new_version_file(version_contents: str, increment_type: str):
    """Parses the version file string, increments the appropriate number, and returns the new string

    Args:
        version_contents: Contents of the version file
        increment_type: What version number to increment (major, minor, patch)

    Returns: Str of the new version file

    """
    lines = version_contents.splitlines()
    new_version_file = ''
    ver = ''
    for line in lines:
        if line.startswith('#') and line.find('RELEASE_VERSION') != -1:
             _,_,ver = line.split(' ')
             ver = semver.VersionInfo.parse(ver.strip("\""))
             if increment_type.lower() == 'patch':
                 ver = ver.bump_patch()
             elif increment_type.lower() == 'minor':
                 ver = ver.bump_minor()
             elif increment_type.lower() == 'major':
                 ver = ver.bump_major()
             else:
                 raise ValueError('Incorrect version type. Options are major, minor, or patch')
             line = f'#define RELEASE_VERSION \"{ver}\"'    
        new_version_file += line + '\n'
    return (ver, new_version_file)

def push_version(file_path: str, git_server: str):#, git_token: str, project_id: int, branch: str, new_version_file: str):
    """Publish the new version file to the Git server

    Args:
        file_path: Path to version file
        git_server: URL of the Git server
        git_token: Access token with permission to write to the Git repo
        project_id: Project id
        branch: Git Branch to save file too
        new_version_file: new version file

    Returns:
        True if push is successful

    """
    print(f'file_path: {file_path}')
    print(f'git_server: {git_server}')
    fp=open(git_server, 'r+')
    fp.seek(0)
    server=fp.read()
    print(server)
    # print(f'git_token: {git_token}')
    # print(f'project_id: {project_id}')
    # print(f'branch: {branch}')
    # gl = gitlab.Gitlab(git_server, private_token=git_token)
    # p = gl.projects.get(project_id)
    # print(f'Working on project {p.name}')
    # try:
    #     f = p.files.get(file_path, branch)
    #     f.content = new_version_file
    #     f.save(branch=branch, commit_message='Incrementing version for release [skip ci]')
    # except gitlab.GitlabGetError as ex:
    #     print(ex)
    #     return False
    return True

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('path', help='Path to version file')
    p.add_argument('increment_type', help='major, minor, or patch', choices=['major', 'minor', 'patch'])
    p.add_argument('--git-server', help='Git server address')
    p.add_argument('--git-token', help='Git deployment token')
    p.add_argument('--git-project_id', help='Project id integer', type=int)
    p.add_argument('--git-branch', help='Which branch to submit the new version file too', default='master')

    args = p.parse_args()

    # Is there a better way of doing this with argparse?
    if args.git_server or args.git_token or args.git_project_id:
        if not (args.git_server and args.git_token and args.git_project_id):
            p.error('If one git_* argument is set they all must be')
    return args

def gen_version(file_path: str, increment_type: str):
    fp = open(file_path, 'r+')
    fp.seek(0)
    (ver, new_file) = generate_new_version_file(fp.read(), increment_type)
    print(ver)
    print(new_file)
    fp.seek(0)
    fp.write(new_file)
    fp.close()
    return 

