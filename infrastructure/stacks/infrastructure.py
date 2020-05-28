from aws_cdk import (
    core,
    aws_dynamodb as dynamo,
    aws_lambda as lambda_,
    aws_ses as ses,
    aws_iam as iam,
    aws_apigateway as ag
)

class InfrastructureStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = dynamo.Table(
            self, 'Table',
            table_name='subscriptions',
            partition_key=dynamo.Attribute(name='pk', type=dynamo.AttributeType.STRING),
            sort_key=dynamo.Attribute(name='sk', type=dynamo.AttributeType.STRING),
            time_to_live_attribute='ttl'
        )

        template_name = 'EmailVerification'
        template = ses.CfnTemplate(self, 'Template',
            template={
                'htmlPart': '<div><a href="{code}">Verify Email</a></div>',
                'subjectPart': 'Verify Email Address',
                'templateName': template_name
            }
        )

        create_subscription = lambda_.Function(
            self, 'CreateSubscriptionFunction',
            function_name='create_subscription',
            handler='src.main.handler',
            code=lambda_.Code.from_asset('../functions/create_subscription'),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={
                'TEMPLATE_NAME': template_name,
                'TABLE_NAME': table.table_name
            }
        )

        # Update Lambda Permissions
        create_subscription.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    'ses:SendEmail',
                    'ses:SendRawEmail'
                ],
                resources=['*']
            )
        )

        table.grant_read_write_data(create_subscription)

        # API
        api = ag.RestApi(self, 'Api', rest_api_name='email-subscriptions')

        subscriptions_resource = api.root.add_resource('subscriptions')

        subscriptions_resource.add_method('POST',
            integration=ag.LambdaIntegration(
                handler=create_subscription,
                proxy=True
            )
        )
