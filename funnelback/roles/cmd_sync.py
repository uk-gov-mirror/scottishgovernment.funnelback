import os

import click

from ..environments import ENVS
from ..worktree import Worktree
from .role import Role, load_role


@click.command()
@click.argument("environment")
@click.option("--dryrun", flag_value=True, type=click.BOOL)
def sync(environment, dryrun):
    env = ENVS[environment]
    worktree = Worktree("roles")
    role_ids = env.get_roles()
    design_files = worktree.design_files(env)

    roles = {}
    for path in design_files.values():
        role = load_role(path, env.client_id)
        roles[path] = role
        id = role.id
        if id not in role_ids and not dryrun:
            env.create_role(id)

    for path in design_files.values():
        role = roles[path]
        state = env.get_role(role.id)
        diff = state.diff(role)
        for d in diff:
            if not dryrun:
                d.apply(env, role.path(env.client_id))
            else:
                print(d)


