import click
from ..environments import ENVS
from .role import Role, load_role
from ..worktree import Worktree


@click.command()
@click.argument("environment")
def drift(environment):
    env = ENVS[environment]
    worktree = Worktree("roles")
    design = worktree.design_files(env)
    for file, path in design.items():
        design_role = load_role(path, env.client_id)
        if worktree.has_state_file(env, file):
            state_role = Role(worktree.read_state(env, file))
            diff_roles(design_role, state_role)
        else:
            print(f"Only in design: {design_role.id}")
    state_files = worktree.state_files(env)
    new_role_files = [file for file in state_files if file not in design]
    for state_file in new_role_files:
        state_role = Role(worktree.read_state(env, state_file))
        print(f"Only in state: {state_role.id}")


def diff_roles(design, state):
    diff = state.diff(design)
    if diff:
        print(f"Role: {design.id}")
        for d in diff:
            print(str(d))


