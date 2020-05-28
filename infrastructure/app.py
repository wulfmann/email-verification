#!/usr/bin/env python3

from aws_cdk import core
from stacks.infrastructure import InfrastructureStack

app = core.App()
InfrastructureStack(app, 'email-verification-infrastructure')

app.synth()
